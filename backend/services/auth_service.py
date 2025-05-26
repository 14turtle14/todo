from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import UTC, datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.database import get_db
from backend.services.user_service import find_user

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def decode_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    payload = await decode_token(token)
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
    return db_user