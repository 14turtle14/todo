from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.models.models import User
from backend.models.schemas.user_schema import UserCreate
import logging
logger = logging.getLogger(__name__)

async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def find_user(db: AsyncSession, user_id: int):
    db_user = await db.execute(select(User).where(User.id == user_id))
    return db_user.scalars().first()

async def delete_user(db: AsyncSession, user_id: int):
    db_user = await find_user(db, user_id)
    await db.delete(db_user)
    await db.commit()
    return db_user

async def get_users(db: AsyncSession):
    db_users = await db.execute(select(User))
    logger.info("cruto!")
    return db_users.scalars().all()

async def get_user_by_email(db: AsyncSession, email: str):
    db_user = await db.execute(select(User).where(User.email == email))
    return db_user.scalars().first()

async def get_user_by_username(db: AsyncSession, username: str):
    db_user = await db.execute(select(User).where(User.username == username))
    return db_user.scalars().first()

async def get_user_by_login(db: AsyncSession, login: str):
    db_user = await get_user_by_username(db, login)
    if db_user:
        return db_user
    db_user = await get_user_by_email(db, login)
    if db_user:
        return db_user
    return None

async def update_user_username(db: AsyncSession, username_new: str, user_id: int):
    if get_user_by_username(db, username=username_new):
        raise HTTPException(status_code=400, detail="Username is taken")
    db_user = await find_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.username = username_new
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user_email(db: AsyncSession, email_new: str, user_id: int):
    if get_user_by_email(db, email=email_new):
        return HTTPException(status_code=400, detail="Email is taken")
    db_user = await find_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.email = email_new
    await db.commit()
    await db.refresh(db_user)
    return db_user