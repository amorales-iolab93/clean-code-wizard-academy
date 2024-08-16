
from fastapi import FastAPI

from app.core.containers import Container
def init_dependences(_app: FastAPI, _ioc: Container) -> None:
    _app.container = _ioc

