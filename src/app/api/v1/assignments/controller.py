from typing import List

from fastapi import APIRouter, Depends

from starlette import status

from app.api.v1.assignments.schemas.response import WizardAssignmentsSchema
from app.core.containers import Container

from app.core.contracts.use_cases.wizard_assignments_interface import WizardAssignmentsUseCaseInterface
from app.core.schemas.exception import NotFoundException,UnprocessableEntity,InternalServerErrorException
from app.use_cases.wizard_assignments import WizardAssignmentsUseCase





assignments_router = APIRouter(
    responses={
        200: {"description": "OK"},
        # 404: {"description": "NotFound Error", "model": NotFoundException},
        # 422: {"description": "Validation Error", "model": UnprocessableEntity},
        # 500: {"description": "Internal Server Error", "model": InternalServerErrorException},
    },
)

@assignments_router.get(
    "", response_model=List[WizardAssignmentsSchema], status_code=status.HTTP_200_OK
)
async def assignments(
  use_case: WizardAssignmentsUseCase = Depends()
)-> List[WizardAssignmentsSchema]:
    """
    Retrieve all wizard assignments.

    This endpoint retrieves all the wizard assignments from the database grouped by grimorie.

    Parameters:
    - use_case: WizardRequestsUseCase (Dependency Injection)

    Returns:
    - response: WizardRequestsSchema
    """
    response: List[WizardAssignmentsSchema] = await use_case.retrieve()
    return response
