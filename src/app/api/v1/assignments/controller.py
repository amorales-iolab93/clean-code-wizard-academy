from typing import List

from fastapi import APIRouter, Depends

from starlette import status

from app.api.v1.assignments.schemas.response import WizardAssignmentsViewModel
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
    "", response_model=List[WizardAssignmentsViewModel], status_code=status.HTTP_200_OK
)
async def assignments(use_case: WizardAssignmentsUseCase = Depends()):
    """
    Retrieve all wizard assignments.

    This endpoint retrieves all the wizard assignments from the database grouped by grimorie.

    Parameters:
    - use_case: WizardRequestsUseCase (Dependency Injection)

    Returns:
    - response: WizardRequestsViewModel
    """
    response: List[WizardAssignmentsViewModel] = await use_case.retrieve()
    return response
