import uvicorn
import logging

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import models, schemas
from app.services import users
from database import SessionLocal, engine
from http.client import HTTPException
from fastapi import FastAPI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

models.Base.metadata.create_all(bind=engine)

logger = logging.getLogger(__name__)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return users.create_user(db, user)

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = users.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

if __name__ == '__main__':
    uvicorn.run(app)