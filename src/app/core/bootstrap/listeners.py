from fastapi import FastAPI


def init_listeners(_app: FastAPI) -> None:
    @_app.on_event("startup")
    async def startup():
        print("To initialize some connections")

    @_app.on_event("shutdown")
    async def shutdown():
        print("To close ")
