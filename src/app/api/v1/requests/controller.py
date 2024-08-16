from fastapi import APIRouter, Body, Depends
from starlette import status
from starlette.responses import Response

from app.api.v1.requests.schemas.request import (
    DeleteParamsRegisterRequestSchema,
    RegisterRequestSchema,
    UpdateParamsRegisterByRequestSchema,
    UpdateParamsRegisterRequestSchema,
    UpdateRegisterRequestSchema,
)
from app.api.v1.requests.schemas.response import WizardRequestsSchema
from app.core.contracts.use_cases.wizard_requests_interface import WizardRequestsUseCaseInterface
from app.core.schemas.exception import NotFoundException,UnprocessableEntity,InternalServerErrorException
from app.use_cases.wizard_requests import WizardRequestsUseCase


requests_router = APIRouter(
    responses={
        200: {"description": "OK"},
        # 404: {"description": "NotFound Error", "model": NotFoundException},
        # 422: {"description": "Validation Error", "model": UnprocessableEntity},
        # 500: {"description": "Internal Server Error", "model": InternalServerErrorException},
    },
)


@requests_router.get("", response_model=WizardRequestsSchema, status_code=status.HTTP_200_OK)
async def requests(
    use_case: WizardRequestsUseCase = Depends()
)->WizardRequestsSchema:
    """
    Retrieve all wizard requests.

    This endpoint retrieves all the wizard requests from the database.

    Parameters:
    - use_case: WizardRequestsUseCase (Dependency Injection)

    Returns:
    - response: WizardRequestsSchema
    """
    response: WizardRequestsSchema = await use_case.retrieve()
    return response


@requests_router.post("")
async def register(
    body: RegisterRequestSchema = Body(), 
    use_case: WizardRequestsUseCase = Depends()
)-> None:
    """
    Register a new wizard request.

    This endpoint registers a new wizard request in the database.

    Parameters:
    - body: RegisterRequestSchema (Request Body)
    - use_case: WizardRequestsUseCase (Dependency Injection)

    Returns:
    - Response with status code 201 CREATED
    """
    try:
        await use_case.create(body)
        return Response(status_code=status.HTTP_201_CREATED)
    except Exception as e:
        raise e




@requests_router.put("/{record_id}")
async def update_request(
    body: UpdateRegisterRequestSchema = Body(),
    params: UpdateParamsRegisterRequestSchema = Depends(),
    use_case: WizardRequestsUseCase = Depends(),
)-> None:
    """
    Update an existing wizard request.

    This endpoint updates an existing wizard request in the database.

    Parameters:
    - record_id: str (Path Parameter)
    - body: UpdateRegisterRequestSchema (Request Body)
    - params: UpdateParamsRegisterRequestSchema (Dependency Injection)
    - use_case: WizardRequestsUseCase (Dependency Injection)

    Returns:
    - Response with status code 200 OK
    """
    await use_case.update(params, body)
    return Response(status_code=status.HTTP_200_OK)


@requests_router.patch("/{record_id}/status/{status}")
async def set_status(
    params: UpdateParamsRegisterByRequestSchema = Depends(), 
    use_case: WizardRequestsUseCase = Depends()
)-> None:
    """
    Update the status of a wizard request.

    This endpoint updates the status of a wizard request in the database.

    Parameters:
    - record_id: str (Path Parameter)
    - status: str (Path Parameter)
    - params: UpdateParamsRegisterByRequestSchema (Dependency Injection)
    - use_case: WizardRequestsUseCase (Dependency Injection)

    Returns:
    - Response with status code 200 OK
    """
    await use_case.update_by(params)
    return Response(status_code=status.HTTP_200_OK)


@requests_router.delete("/{record_id}")
async def remove(
    params: DeleteParamsRegisterRequestSchema = Depends(), 
    use_case: WizardRequestsUseCase = Depends()
)-> None:
    """
    Delete a wizard request.

    This endpoint deletes a wizard request from the database.

    Parameters:
    - record_id: str (Path Parameter)
    - params: DeleteParamsRegisterRequestSchema (Dependency Injection)
    - use_case: WizardRequestsUseCase (Dependency Injection)

    Returns:
    - Response with status code 200 OK
    """
    await use_case.delete(params)
    return Response(status_code=status.HTTP_200_OK)
