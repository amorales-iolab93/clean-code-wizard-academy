from enum import Enum
from http import HTTPStatus


class ResponseStatus(Enum):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


    REQUEST_REGISTERED_ERROR = (HTTPStatus.BAD_REQUEST, "Could not register the request")
    REQUEST_NOT_FOUND = (HTTPStatus.NOT_FOUND, "Request not found")
    REQUEST_ALREADY_EXIST = (HTTPStatus.NO_CONTENT, "Request already exist")
    

