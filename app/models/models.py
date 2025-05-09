from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, index=True)
    targets = relationship("Target", back_populates="owner")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    deadline = Column(Date())
    is_done = Column(Boolean)
    target_id = Column(Integer, ForeignKey("targets.id"))  
    target = relationship("Target", back_populates="tasks")

class Target(Base):
    __tablename__ = "targets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    deadline = Column(Date())
    is_done = Column(Boolean)
    owner_id = Column(Integer, ForeignKey("users.id"))  
    owner = relationship("User", back_populates="targets")
    tasks = relationship("Task", back_populates="target")
    