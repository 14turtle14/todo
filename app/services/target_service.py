from sqlalchemy.orm import AsyncSession
from app.models.models import Target
from sqlalchemy.future import select
from app.models.schemas.target_schema import TargetCreate, TargetUpdate

async def create_target(db: AsyncSession, target: TargetCreate, user_id: int):
    db_target = Target(**target, owner_id=user_id)
    db.add(db_target)
    await db.commit()
    await db.refresh(db_target)
    return db_target

async def find_target(db: AsyncSession, target_id: int, user_id: int):
    return await db.execute(select(Target).where(Target.id == target_id and Target.owner_id == user_id)).scalars().first()

async def delete_target(db: AsyncSession, target_id: int, user_id: int):
    db_target = await find_target(db, target_id, user_id)
    db.delete(db_target)
    await db.commit()
    await db.refresh(db_target)
    return db_target

async def get_targets(db: AsyncSession, user_id: int):
    return await db.execute(select(Target).where(Target.owner == user_id)).scalars().all()

async def update_target(target: TargetUpdate, target_id: int, db: AsyncSession, user_id: int):
    db_target = find_target(db, target_id, user_id)
    for field, value in target.model_dump(exclude_unset=True).items():
            setattr(db_target, field, value)
        
    await db.commit()
    await db.refresh(db_target)
    return db_target