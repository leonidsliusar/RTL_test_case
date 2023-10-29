from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class AggregateType(str, Enum):
    hour = "hour"
    day = "day"
    week = "week"
    month = "month"


class InputModel(BaseModel):
    dt_from: datetime
    dt_upto: datetime
    group_type: AggregateType


class OutputModel(BaseModel):
    dataset: list
    labels: list[datetime]
