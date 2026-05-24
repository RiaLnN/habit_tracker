from app.database import Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List
from datetime import date

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)

    habits: Mapped[List["Habit"] | None] = relationship(back_populates="user", cascade="all, delete-orphan")

class Habit(Base):
    __tablename__ = "habits"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="habits")
    
    checks: Mapped[List["HabitCheck"]] = relationship(back_populates="habit", cascade="all, delete-orphan")

class HabitCheck(Base):
    __tablename__ = "habit_checks"

    id: Mapped[int] = mapped_column(primary_key=True)
    check_date: Mapped[date] = mapped_column(default=date.today())
    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id"))

    habit: Mapped["Habit"] = relationship(back_populates="checks")

