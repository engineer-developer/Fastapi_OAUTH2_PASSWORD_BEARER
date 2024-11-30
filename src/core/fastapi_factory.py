from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse


def create_app() -> FastAPI:
    from src.database.utils import alembic_upgrade_head
    from src.api.v1 import router as api_v1_router

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        is_successful_upgrade = alembic_upgrade_head()
        if not is_successful_upgrade:
            exit(1)
        yield

    fastapi_app = FastAPI(
        lifespan=lifespan,
        default_response_class=ORJSONResponse,
        title="Basic auth sample",
        description="__FastAPI_basic_auth__",
        version="0.0.1",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    fastapi_app.include_router(api_v1_router)

    @fastapi_app.get("/api", response_class=ORJSONResponse, tags=["Check api"])
    async def get_first():
        return {"status": "Successful run"}

    return fastapi_app
