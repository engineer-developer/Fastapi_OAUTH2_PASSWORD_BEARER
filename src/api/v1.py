from fastapi import APIRouter

from src.dto.users.crud import router as users_router

router = APIRouter(prefix="/api")


router.include_router(users_router)
