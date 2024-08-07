from fastapi import FastAPI

from app.api.v1 import router as api_v1_router


def init_routers(_app: FastAPI) -> None:
    _app.include_router(api_v1_router)
