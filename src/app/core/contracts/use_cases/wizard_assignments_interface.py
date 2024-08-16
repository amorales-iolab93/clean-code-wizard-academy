from abc import ABC, abstractmethod
from typing import List
from app.api.v1.assignments.schemas.response import WizardAssignmentsSchema
from app.core.contracts.use_cases.core import WizardAssignmentImpl


class WizardAssignmentsUseCaseInterface(WizardAssignmentImpl[WizardAssignmentsSchema],ABC):

    @abstractmethod
    async def retrieve(self) -> List[WizardAssignmentsSchema]:
        pass

