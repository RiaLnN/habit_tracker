from pydantic import BaseModel, ConfigDict, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserResponse(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)