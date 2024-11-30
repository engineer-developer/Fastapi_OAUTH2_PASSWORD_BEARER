from fastapi import APIRouter

from src.dto.clients.crud import router as clients_router

router = APIRouter(prefix="/api")


router.include_router(clients_router)
