
from app.schemas.auth import UserCreate
from app.models import User
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core import security
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from app.database import get_session
from typing import Annotated
import jwt

def user_exist(data: UserCreate, session: Session) -> bool:
    res = session.execute(
        select(User)
        .where(User.email == data.email)
    ).scalar_one_or_none()

    return res is not None

def save_user(data: UserCreate, session: Session) -> User | None:
    if (user_exist(data, session)): return None
    
    hashed_password = security.hash_password(data.password)
    new_user = User(
        email=data.email,
        hashed_password=hashed_password,
        )
    session.add(new_user)
    session.commit()
    return new_user

def get_user_by_id(id: int | None, session: Session) -> User | None:
    user = session.execute(
        select(User)
        .where(User.id == id)
    ).scalar_one_or_none()
    return user


def login_user(data: UserCreate, session: Session) -> User | None:
    user = session.execute(
        select(User)
        .where(User.email == data.email)
    ).scalar_one_or_none()

    if user is not None and security.check_hash_password(data.password, user.hashed_password):
        return user
    
    return None

def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security.security)],
    session: Annotated[Session, Depends(get_session)]
) -> User:
    token = credentials.credentials
    try:
        payload = security.get_payload(token)
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token claims")
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        
    user = get_user_by_id(user_id, session)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    return user