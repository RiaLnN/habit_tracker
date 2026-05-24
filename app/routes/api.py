from fastapi import APIRouter
from app.routes import auth_routes

router = APIRouter()

router.include_router(auth_routes.router, tags=["auth"], prefix="/auth")

