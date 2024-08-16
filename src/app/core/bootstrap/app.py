from fastapi import Depends, FastAPI

from app.core.config.config import Settings, get_settings
from app.core.containers import Container

from .ioc import  init_dependences
from .listeners import init_listeners
from .routers import init_routers
from .handlers import init_handlers


def create_app() -> FastAPI:
    settings: Settings = get_settings()
    _ioc = Container()
    _ioc.wire(modules=[__name__])
    _app = FastAPI(
        title=settings.PROJECT_TITLE,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.PROJECT_VERSION,
    )

    init_dependences(_app=_app, _ioc =_ioc)
    init_listeners(_app=_app)
    init_handlers(_app=_app)
    init_routers(_app=_app)

    return _app
