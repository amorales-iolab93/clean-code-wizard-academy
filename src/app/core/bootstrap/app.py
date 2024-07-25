from fastapi import FastAPI

from app.core.config.config import Settings, get_settings

from .listeners import init_listeners
from .routers import init_routers
from .handlers import init_handlers


def create_app() -> FastAPI:
    settings: Settings = get_settings()

    _app = FastAPI(
        title=settings.PROJECT_TITLE,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.PROJECT_VERSION,
    )

    init_listeners(_app=_app)
    init_handlers(_app=_app)
    init_routers(_app=_app)

    return _app
