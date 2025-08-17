from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import UTC, datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Response

from database.database import get_db
from models.models import RefreshToken
from models.schemas.user_schema import RefreshTokenCreate
from services.user_service import find_user

token_blacklist = set()

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def add_to_blacklist(token: str):
    token_blacklist.add(token)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(user_id: int) -> str:
    expires = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expires, "type": "access"}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def create_refresh_token(user_id: int, db: AsyncSession = Depends(get_db)):
    await delete_refresh_token(user_id=user_id, db=db)
    expires = datetime.now(UTC) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {"sub": str(user_id), "exp": expires, "type": "refresh"}
    token = RefreshTokenCreate(token=jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM), expires=expires, user_id=user_id)
    
    db_token = RefreshToken(**token.model_dump())
    db.add(db_token)
    await db.commit()
    await db.refresh(db_token)
    response = Response()
    response.set_cookie(
        key="refresh_token",
        value=db_token.token,
        httponly=True,
        secure=True,  
        samesite="strict", 
        max_age=7*24*60*60,  
        path="/refresh"
    )

async def verify_token(token: str = Depends(oauth2_scheme)):
    if token in token_blacklist:
        raise HTTPException(status_code=401, detail="Token revoked")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    payload = await verify_token(token)
    user_id  = payload.get("sub")
    if user_id:
        user = await find_user(db, int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.id

async def change_user_password(password_old: str, password_new: str, user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await find_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(password_old, db_user.password):
        raise HTTPException(status_code=400, detail="Password is invalid")
    if verify_password(password_new, db_user.password):
        raise HTTPException(status_code=400, detail="Old and new passwords are the same")
    db_user.password = get_password_hash(password_new)
    await db.commit()
    await db.refresh(db_user)
    await delete_refresh_token(user_id = db_user.id)
    return db_user

async def check_refresh_token(refresh_token: str, user_id: int, db: AsyncSession = Depends(get_db)):
    db_token = await db.execute(select(RefreshToken).where(RefreshToken.user_id == user_id, RefreshToken.token == refresh_token))
    return db_token.scalars().first()

async def delete_refresh_token(user_id: int, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    add_to_blacklist(token)
    db_token = await db.execute(select(RefreshToken).where(RefreshToken.user_id == user_id))
    db_token = db_token.scalars().first()
    if db_token:
        await db.delete(db_token)
        await db.commit()