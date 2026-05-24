from fastapi import APIRouter, Depends, HTTPException
from app.services.auth import save_user, login_user
from app.core.security import create_jwt
from app.schemas.auth import UserCreate, UserResponse
from sqlalchemy.orm import Session
from typing import Annotated
from app.database import get_session

router = APIRouter()

@router.post('/register', response_model=UserResponse)
def register(data: UserCreate, session: Annotated[Session, Depends(get_session)]):
    user = save_user(data=data, session=session)
    if user is not None:
        return {"token": create_jwt(user.id)}
    else:
        raise HTTPException(status_code=400, detail="User already exist")


@router.post('/login', response_model=UserResponse)
def login(data: UserCreate, session: Annotated[Session, Depends(get_session)]):
    user = login_user(data=data, session=session)
    if user is not None:
        return {"token": create_jwt(user.id)}
    else:
        raise HTTPException(status_code=401, detail="Wrong user data")
    
