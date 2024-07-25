
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from collections import defaultdict

from app.core.schemas.exception import BadRequestException, BaseCustomException, UnprocessableEntity


def init_handlers(_app: FastAPI) -> None:

    @_app.exception_handler(BaseCustomException)
    async def custom_exception_handler(request: Request, exc: BaseCustomException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": exc.status,
                "status_type": exc.status_type,
                "message": exc.message
            },
        )

    @_app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        reformatted_message = defaultdict(list)
        field_string = ''
        msg = ''

        for pydantic_error in exc.errors():
            loc, msg, error_type = pydantic_error["loc"], pydantic_error["msg"], pydantic_error["type"]

            if error_type == "value_error.jsondecode":
                return await custom_exception_handler(request=request, exc=BadRequestException())

            filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") and loc[1:] else loc
            field_string = ".".join(filtered_loc)
            reformatted_message[field_string].append(msg)

        return JSONResponse(
            status_code=UnprocessableEntity().status_code,
            content={
                "status": UnprocessableEntity.status,
                "status_type": UnprocessableEntity.status_type,
                "message": field_string.capitalize() + ' ' + msg,
                "errors": reformatted_message
            }
        )