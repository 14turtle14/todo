from sqlalchemy.orm import Session

from app.models.schemas.target_schema import TargetCreate, TargetUpdate
from . import models

def create_target(db: Session, target: TargetCreate):
    db_target = models.Target(**target)
    db.add(db_target)
    db.commit()
    db.refresh(db_target)
    return db_target

def find_target(db: Session, target_id: int):
    return db.query(models.Target).filter(models.Target.id == target_id).first()

def delete_target(db: Session, target_id: int):
    db_target = find_target(db, target_id)
    db.delete(db_target)
    db.commit()
    return db_target

def get_targets(db: Session):
    return db.query(models.Target).all()

def update_target(db: Session, target: TargetUpdate, target_id: int):
    db_target = find_target(db, target_id)
    for field, value in target.model_dump().items():
            setattr(db_target, field, value)
        
    db.commit()
    db.refresh(db_target)
    return db_target