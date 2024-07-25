from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

from fastapi import Depends

from app.api.v1.assignments.schemas.response import WizardAssignmentsViewModel
from app.services.wizard.report_service import ReportService
from app.use_cases.core.base import WizardAssignmentImpl


class WizardAssignmentsUseCase(WizardAssignmentImpl[WizardAssignmentsViewModel]):
    def __init__(self, report_service: ReportService = Depends()):
        self.report_service: ReportService = report_service

    async def retrieve(self) -> List[WizardAssignmentsViewModel]:
        retrieve_record = await self.report_service.retrieve_assignments()
        return retrieve_record



