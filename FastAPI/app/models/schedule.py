from datetime import datetime
from enum import Enum

from pydantic import BaseModel

class ScheduleStatusEnum(str, Enum):
    AVAILABLE = "Available"
    UNAVAILABLE = "Unavailable"

class Schedule(BaseModel):
    id: int
    openingTime: datetime
    closingTime: datetime
    status: ScheduleStatusEnum