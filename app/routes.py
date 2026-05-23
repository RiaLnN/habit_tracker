from fastapi import APIRouter

router = APIRouter()


@router.post('/auth/register')
def save_user():
    pass