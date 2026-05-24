
from app.schemas.auth import UserCreate
from app.models import User
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core import security
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends

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

def get_current_user(session: Session, credentials: HTTPAuthorizationCredentials = Depends(security.security)) -> User | None:
    token = credentials.credentials
    payload = security.get_payload(token)
    user = get_user_by_id(payload.get("user_id"), session)
    return user