from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import User, Habit, HabitCheck
from app.schemas.habits import HabitCreate
from sqlalchemy.exc import IntegrityError
from datetime import timedelta, date

def create_habit(user: User, data_in: HabitCreate, session: Session) -> Habit:
    new_habit = Habit(
        title=data_in.title,
        user_id=user.id,
        user=user
    )
    session.add(new_habit)
    session.commit()
    return new_habit

def get_habits(user: User, session: Session):
    habbits = session.execute(
        select(Habit)
        .where(Habit.user_id == user.id)
    ).scalars().all()
    return habbits

def get_habit_by_id(habit_id: int, session: Session) -> Habit | None:
    habbit = session.execute(
        select(Habit)
        .where(Habit.id == habit_id)
    ).scalar_one_or_none()
    return habbit

def create_habit_check(habit_id: int, user: User, session: Session) -> HabitCheck:
    habit = get_habit_by_id(habit_id=habit_id, session=session)
    
    if habit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habit dont exist")
    
    if habit.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User dont own the habit")
    
    new_check = HabitCheck(
        habit_id=habit_id,
        habit=habit
    )

    session.add(new_check)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="You have already checked this habit today"
        )
    return new_check

def evaluate_streak(checks: list[HabitCheck]) -> int:
    if not checks:
        return 0

    dates = sorted({c.check_date for c in checks}, reverse=True)
    
    today = date.today()
    yesterday = today - timedelta(days=1)
    
    if dates[0] < yesterday:
        return 0
        
    streak = 1
    for i in range(len(dates) - 1):
        if dates[i] - timedelta(days=1) == dates[i + 1]:
            streak += 1
        else:
            break 
            
    return streak


def get_habit_stats(habit_id: int, user: User, session: Session) -> int:
    habit = get_habit_by_id(habit_id, session)

    if habit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habit dont exist")
    
    if habit.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User dont own the habit")
    
    if habit.checks:
        return evaluate_streak(habit.checks)
    
    return 0