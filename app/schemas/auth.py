from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    pass

class UserCreate(UserBase):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    token: str