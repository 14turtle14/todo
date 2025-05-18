from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.models.models import Target
from backend.models.schemas.target_schema import TargetCreate, TargetUpdate

async def create_target(db: AsyncSession, target: TargetCreate, user_id: int):
    db_target = Target(**target.model_dump(), user_id=user_id)
    db.add(db_target)
    await db.commit()
    await db.refresh(db_target)
    return db_target

async def find_target(db: AsyncSession, target_id: int, user_id: int):
    db_target = await db.execute(select(Target).where(Target.id == target_id, Target.user_id == user_id))
    return db_target.scalars().first()

async def delete_target(db: AsyncSession, target_id: int, user_id: int):
    db_target = await find_target(db, target_id, user_id)
    await db.delete(db_target)
    await db.commit()
    await db.refresh(db_target)
    return db_target

async def get_targets(db: AsyncSession, user_id: int):
    db_targets = await db.execute(select(Target).where(Target.user_id == user_id))
    return db_targets.scalars().all()

async def update_target(db: AsyncSession, target: TargetUpdate, target_id: int, user_id: int):
    db_target = find_target(db, target_id, user_id)
    for field, value in target.model_dump(exclude_unset=True).items():
        setattr(db_target, field, value)
        
    await db.commit()
    await db.refresh(db_target)
    return db_target