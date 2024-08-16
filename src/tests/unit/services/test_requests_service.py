import pytest
from app.core.contracts.services.requests_service_interface import RequestsServiceInterface
from app.services.wizard.requests_service import RequestsService




@pytest.mark.asyncio
async def test_create_request(mock_request_repository):
    # Arrange 
    # SetUp Mocks
    report_service:RequestsServiceInterface = RequestsService(
        db_repository =  mock_request_repository
    )
    # Act 
    # init repository with mocks an execute artefact
    retrieve_assignments = await report_service.create_request()
    # Assert 
    assert not isinstance(retrieve_assignments, Exception)
    

@pytest.mark.asyncio
async def test_update_request(mock_request_repository):
    #TODO: Continue test
    # Arrange 
    # SetUp Mocks
    # report_service:RequestsServiceInterface = RequestsService(
    #     db_repository =  mock_request_repository
    # )
    # params = UpdateParamsRegisterRequestSchema(
    #     record_id = "323b5cca-b124-4883-9212-00438cfd78b4"
    # )
    # payload = UpdateRegisterRequestSchema(

    # )
    # # Act 
    # # init repository with mocks an execute artefact
    # retrieve_assignments = await report_service.update_request(params,payload)
    # # Assert 
    # assert not isinstance(retrieve_assignments, Exception)
    pass

@pytest.mark.asyncio
async def test_update_by_request(mock_request_repository):
    pass

@pytest.mark.asyncio
async def test_delete_request(mock_request_repository):
    pass
