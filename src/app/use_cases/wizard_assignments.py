
from typing import List

from fastapi import Depends
from app.api.v1.assignments.schemas.response import WizardAssignmentsSchema
from app.core.contracts.services.report_service_interface import ReportServiceInterface
from app.core.contracts.use_cases.wizard_assignments_interface import WizardAssignmentsUseCaseInterface
from app.services.wizard.report_service import ReportService



class WizardAssignmentsUseCase(WizardAssignmentsUseCaseInterface):
    def __init__(self, report_service: ReportService = Depends()):
        self.report_service: ReportServiceInterface = report_service

    async def retrieve(self) -> List[WizardAssignmentsSchema]:
        retrieve_record = await self.report_service.retrieve_assignments()
        return retrieve_record



