from typing import Optional
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

from models.schemas.target_schema import TargetType 

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()

    targets: Mapped[list["Target"]] = relationship(back_populates="user", cascade="all, delete-orphan", lazy="selectin")
    tokens: Mapped[list["RefreshToken"]] = relationship(back_populates="user", cascade="all, delete-orphan", lazy="selectin")

class Target(Base):
    __tablename__ = "targets"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    type: Mapped[TargetType] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    deadline: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    interval_days: Mapped[Optional[int]] = mapped_column(nullable=True)
    last_repeated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship(back_populates="targets", lazy="selectin")
    tasks: Mapped[list["Task"]] = relationship(back_populates="target",  cascade="all, delete-orphan", lazy="selectin")

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    is_done: Mapped[bool] = mapped_column()
    is_priorityzed: Mapped[bool] = mapped_column()
    target_id: Mapped[int] = mapped_column(ForeignKey("targets.id"))

    target: Mapped["Target"] = relationship(back_populates="tasks", lazy="selectin")

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column()
    expires: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))  
    user: Mapped["User"] = relationship(back_populates="tokens", lazy="selectin")
    