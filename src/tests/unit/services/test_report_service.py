import pytest
from app.api.v1.assignments.schemas.response import WizardAssignmentsSchema
from app.api.v1.requests.schemas.response import WizardRequestsRecord
from app.core.contracts.services.report_service_interface import ReportServiceInterface
from app.services.wizard.report_service import ReportService

@pytest.mark.asyncio
async def test_retrieve_assignments(mock_report_repository):
    # Arrange 
    # SetUp Mocks
    report_service:ReportServiceInterface = ReportService(
        db_repository =  mock_report_repository
    )
    # Act 
    # init repository with mocks an execute artefact
    retrieve_assignments = await report_service.retrieve_assignments()
    # Assert 
    for item in retrieve_assignments:
        assert isinstance(item, WizardAssignmentsSchema)
    
@pytest.mark.asyncio
async def test_retrieve_requests(mock_report_repository):
    # Arrange 
    # SetUp Mocks
    report_service:ReportServiceInterface = ReportService(
        db_repository =  mock_report_repository
    )
    # Act 
    # init repository with mocks an execute artefact
    retrieve_request = await report_service.retrieve_requests()
    # Assert 
    assert retrieve_request.size == len(retrieve_request.request)
    for item in retrieve_request.request:
        assert isinstance(item, WizardRequestsRecord)
