from itertools import groupby
from operator import attrgetter
from typing import List, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class DataHelper:
    @staticmethod
    def group_by_attribute(records: List[T], attribute: str) -> dict:
        filtered_records = [
            record for record in records if getattr(record, attribute, None) is not None
        ]
        filtered_records.sort(key=attrgetter(attribute))
        grouped_records = {
            key: list(group) for key, group in groupby(filtered_records, key=attrgetter(attribute))
        }
        return grouped_records
