from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from src.dto.users.crud import router as users_router

router = APIRouter(prefix="/api")


router.include_router(users_router)


@router.get("", response_class=ORJSONResponse, tags=["Api"])
async def get_api_version():
    return {"api_version": "v1"}
