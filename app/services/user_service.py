from sqlalchemy.orm import AsyncSession
from sqlalchemy.future import select
from app.models.models import User
from app.models.schemas.user_schema import UserCreate, UserUpdate

async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(**user)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def find_user(db: AsyncSession, user_id: int):
    return await db.execute(select(User).where(User.id == user_id)).scalars().first()

async def delete_user(db: AsyncSession, user_id: int):
    db_user = await find_user(db, user_id)
    db.delete(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_users(db: AsyncSession):
    return await db.execute(select(User)).scalars().all()

async def update_user(db: AsyncSession, user: UserUpdate, user_id: int):
    db_user = await find_user(db, user_id)
    for field, value in user.model_dump(exclude_unset=True).items():
            setattr(db_user, field, value)
        
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_email(db: AsyncSession, email: str):
    return await db.execute(select(User).where(User.email == email)).scalars().first()

async def get_user_by_username(db: AsyncSession, username: str):
    return await db.execute(select(User).where(User.username == username)).scalars().first()

async def get_user_by_login(db: AsyncSession, login: str):
     user = await get_user_by_login(db, login)
     if user:
          return await get_user_by_email(db, login)
     return user