from http import HTTPStatus

from app.core.enum.status_type import StatusType

class BaseCustomException(Exception):
    status: str
    status_type: str
    message: str
    _status_code: int

    class Config:
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True

    @property
    def status_code(self):
        return self._status_code


class BadRequestException(BaseCustomException):
    status = StatusType.ERROR.value
    status_type = HTTPStatus.BAD_REQUEST.name
    message = HTTPStatus.BAD_REQUEST.phrase
    _status_code = HTTPStatus.BAD_REQUEST.value


class NotFoundException(BaseCustomException):
    status = StatusType.ERROR.value
    status_type = HTTPStatus.NOT_FOUND.name
    message = HTTPStatus.NOT_FOUND.phrase
    _status_code = HTTPStatus.NOT_FOUND.value

class InternalServerErrorException(BaseCustomException):
    status = StatusType.ERROR.value
    status_type = HTTPStatus.INTERNAL_SERVER_ERROR.name
    message = HTTPStatus.INTERNAL_SERVER_ERROR.phrase
    _status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value

class ForbiddenException(BaseCustomException):
    status = StatusType.ERROR.value
    status_type = HTTPStatus.FORBIDDEN.name
    message = HTTPStatus.FORBIDDEN.phrase
    _status_code = HTTPStatus.FORBIDDEN.value


class UnauthorizedException(BaseCustomException):
    status = StatusType.ERROR.value
    status_type = HTTPStatus.UNAUTHORIZED.name
    message = HTTPStatus.UNAUTHORIZED.phrase
    _status_code = HTTPStatus.UNAUTHORIZED.value


class UnprocessableEntity(BaseCustomException):
    status = StatusType.ERROR.value
    status_type = HTTPStatus.UNPROCESSABLE_ENTITY.name
    message = HTTPStatus.UNPROCESSABLE_ENTITY.phrase
    _status_code = HTTPStatus.UNPROCESSABLE_ENTITY.value


class DuplicateValueException(BaseCustomException):
    status = StatusType.ERROR.value
    status_type = HTTPStatus.UNPROCESSABLE_ENTITY.name
    message = HTTPStatus.UNPROCESSABLE_ENTITY.phrase
    _status_code = HTTPStatus.UNPROCESSABLE_ENTITY.value