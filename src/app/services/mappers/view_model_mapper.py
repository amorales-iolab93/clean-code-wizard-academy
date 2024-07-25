from typing import List, Tuple

from app.api.v1.assignments.schemas.response import WizardAssignmentsViewModel
from app.api.v1.requests.schemas.response import (
    WizardRequestsRecord,
    WizardRequestsViewModel,
)
from app.core.utils import data_utils
from app.models.view.view_wizard_request import ViewWizardRequest


class ViewModelMapper:
    @staticmethod
    def mapper_to_view_assignments(
        retrieve_list: List[ViewWizardRequest],
    ) -> List[WizardAssignmentsViewModel]:
        grouped_records = data_utils.DataHelper.group_by_attribute(retrieve_list, "grimorie")
        result: List[WizardAssignmentsViewModel] = []
        for index, group in grouped_records.items():
            grouped_items = [record.dict(by_alias=False) for record in group]
            result.append(
                WizardAssignmentsViewModel(
                    **{"size": len(grouped_items), "grimorie": index, "assignments": grouped_items}
                )
            )
        return result

    @staticmethod
    def mapper_to_view_requests(retrieve_list: List[ViewWizardRequest]) -> WizardRequestsViewModel:
        result: WizardRequestsViewModel = WizardRequestsViewModel(
            size=len(retrieve_list),
            requests=[
                WizardRequestsRecord(**record.dict(by_alias=False)) for record in retrieve_list
            ],
        )
        return result
