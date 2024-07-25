from datetime import datetime

import pytz


class DateTimeHelper:
    @staticmethod
    def now(timezone="America/Mexico_City"):
        tz = pytz.timezone(timezone)
        current_datetime = datetime.now(tz=tz)
        return current_datetime

    @staticmethod
    def now_timestamp(timezone="America/Mexico_City") -> int:
        tz = pytz.timezone(timezone)
        current_datetime = datetime.now(tz=tz)
        current_timestamp = int(current_datetime.timestamp())
        return current_timestamp

    @staticmethod
    def to_datetime(timestamp, timezone="America/Mexico_City"):
        tz = pytz.timezone(timezone)
        datetime_obj = datetime.fromtimestamp(timestamp, tz)
        return datetime_obj
