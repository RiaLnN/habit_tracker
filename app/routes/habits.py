from fastapi import APIRouter, Depends, HTTPException
from app.schemas.habits import HabitCreate, HabitResponse, HabitCheckResponse
from app.services.auth import get_current_user
from app.database import get_session
from app.models import User
from sqlalchemy.orm import Session
from app.services import habits
from typing import List, Annotated

router = APIRouter()

@router.post("", response_model=HabitResponse)
def create_habit(
    data_in: HabitCreate, 
    current_user: Annotated[User, Depends(get_current_user)], 
    session: Annotated[Session, Depends(get_session)]
):
    data = habits.create_habit(user=current_user, data_in=data_in, session=session)
    
    if data is None:
        raise HTTPException(status_code=400, detail="Habit is not created")
    
    return data


@router.get("", response_model=List[HabitResponse])
def get_habits(
    current_user: Annotated[User, Depends(get_current_user)], 
    session: Annotated[Session, Depends(get_session)]
):
    data = habits.get_habits(user=current_user, session=session)

    if data is None:
        raise HTTPException(status_code=400, detail="Habits not found")
    
    return data

@router.post("/{habit_id}/check", response_model=HabitCheckResponse)
def create_habit_check(
    habit_id: int,
    current_user: Annotated[User, Depends(get_current_user)], 
    session: Annotated[Session, Depends(get_session)]
):
    habit_check = habits.create_habit_check(habit_id=habit_id, user=current_user, session=session)
    return habit_check


@router.get("/{habit_id}/stats")
def get_habit_stats(
    habit_id: int,
    current_user: Annotated[User, Depends(get_current_user)], 
    session: Annotated[Session, Depends(get_session)]
):
    streak = habits.get_habit_stats(habit_id=habit_id, user=current_user, session=session)
    return {"streak": streak}