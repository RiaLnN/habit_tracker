from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date

class HabitBase(BaseModel):
    title: str

class HabitCreate(HabitBase):
    pass

class HabitResponse(HabitBase):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)

class HabitCheckBase(BaseModel):
    pass

class HabitCheckResponse(HabitCheckBase):
    id: int
    habit_id: int
    check_date: date
    model_config = ConfigDict(from_attributes=True)