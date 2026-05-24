from fastapi import APIRouter
from app.routes import auth_routes, habits

router = APIRouter()

router.include_router(auth_routes.router, tags=["auth"], prefix="/auth")
router.include_router(habits.router, tags=["habits"], prefix="/habits")
