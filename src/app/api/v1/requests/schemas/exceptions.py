from app.core.enum.response_status import ResponseStatus
from app.core.enum.status_type import StatusType
from app.core.schemas.exception import BaseResponse


class WizardRegisteredException(BaseResponse):
    status: str = StatusType.SUCCESS.value
    status_type: str = ResponseStatus.REQUEST_REGISTERED_ERROR.name
    message: str = ResponseStatus.REQUEST_REGISTERED_ERROR.message
    _status_code: int = ResponseStatus.REQUEST_REGISTERED_ERROR.status_code
