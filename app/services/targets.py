from sqlalchemy.orm import Session
from . import models, schemas

def create_target(db: Session, target: schemas.TargetCreate):
    db_target = models.Target(**target.dict())
    db.add(db_target)
    db.commit()
    db.refresh(db_target)
    return db_target

def get_target(db: Session, target_id: int):
    return db.query(models.Target).filter(models.Target.id == target_id).first()