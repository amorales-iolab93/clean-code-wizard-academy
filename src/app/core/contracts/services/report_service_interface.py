from abc import ABC, abstractmethod
from typing import List
from app.api.v1.assignments.schemas.response import WizardAssignmentsSchema
from app.api.v1.requests.schemas.response import WizardRequestsSchema
from app.models.views import view_wizard_request


class ReportServiceInterface(ABC):

    @abstractmethod
    async def retrieve_assignments(self, disabled=False) -> List[WizardAssignmentsSchema]:
        pass

    @abstractmethod
    async def retrieve_requests(self, disabled=False) -> WizardRequestsSchema:
        pass

