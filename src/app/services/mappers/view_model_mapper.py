from typing import List, Tuple

from app.api.v1.assignments.schemas.response import WizardAssignmentsSchema
from app.api.v1.requests.schemas.response import (
    WizardRequestsRecord,
    WizardRequestsSchema,
)
from app.core.utils import data_utils
from app.models.views.view_wizard_request import ViewWizardRequest


class ViewModelMapper:
    @staticmethod
    def mapper_to_view_assignments(
        retrieve_list: List[ViewWizardRequest],
    ) -> List[WizardAssignmentsSchema]:
        grouped_records = data_utils.DataHelper.group_by_attribute(retrieve_list, "grimorie")
        result: List[WizardAssignmentsSchema] = []
        for index, group in grouped_records.items():
            grouped_items = [record.dict(by_alias=False) for record in group]
            result.append(
                WizardAssignmentsSchema(
                    **{"size": len(grouped_items), "grimorie": index, "assignments": grouped_items}
                )
            )
        return result

    @staticmethod
    def mapper_to_view_requests(retrieve_list: List[ViewWizardRequest]) -> WizardRequestsSchema:
        result: WizardRequestsSchema = WizardRequestsSchema(
            size=len(retrieve_list),
            requests=[
                WizardRequestsRecord(**record.dict(by_alias=False)) for record in retrieve_list
            ],
        )
        return result
