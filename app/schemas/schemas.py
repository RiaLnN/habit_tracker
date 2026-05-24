from pydantic import BaseModel, EmailStr
from typing import Optional, List



class HabitBase(BaseModel):
    title: str

class HabitChecksBase(BaseModel):
    pass

class HabitChecksResponse(HabitChecksBase):
    pass
class HabitCreate(HabitBase):
    pass

class HabitResponse(HabitBase):
    id: int
    user_id: int
    checks: Optional[HabitChecksResponse | None]


