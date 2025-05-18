from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.models.models import User
from backend.models.schemas.user_schema import UserCreate, UserUpdate

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
    await db.refresh(db_user)
    return db_user

async def get_users(db: AsyncSession):
    db_users = await db.execute(select(User))
    return db_users.scalars().all()

async def update_user(db: AsyncSession, user: UserUpdate, user_id: int):
    db_user = await find_user(db, user_id)
    for field, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, field, value)
        
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_email(db: AsyncSession, email: str):
    db_user = await db.execute(select(User).where(User.email == email))
    return db_user.scalars().first()

async def get_user_by_username(db: AsyncSession, username: str):
    db_user = await db.execute(select(User).where(User.username == username))
    return db_user.scalars().first()

async def get_user_by_login(db: AsyncSession, login: str):
    db_user = await get_user_by_login(db, login)
    if db_user:
        return await get_user_by_email(db, login)
    return db_user