"""
This module defines the `Schedule` model and the `ScheduleStatusEnum` enumeration.

The `Schedule` model includes attributes such as ID, opening and closing times, and status.

Classes:
    ScheduleStatusEnum: Enumeration for the status of a schedule.
    Schedule: Represents a schedule with various attributes.
"""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel
from pydantic.v1.class_validators import Validator, validator, root_validator


class ScheduleStatusEnum(str, Enum):
    """
    Enumeration for the status of a schedule.

    Attributes:
        AVAILABLE (str): Indicates the schedule is available.
        UNAVAILABLE (str): Indicates the schedule is unavailable.
    """
    AVAILABLE = "Available"
    UNAVAILABLE = "Unavailable"

class Schedule(BaseModel):
    """
    Represents a schedule with details such as opening and closing times,
    and the current status.

    Attributes:
        id (int): The unique identifier for the schedule.
        opening_time (datetime): The opening time of the schedule.
        closing_time (datetime): The closing time of the schedule.
        status (ScheduleStatusEnum): The current status of the schedule.
    """
    opening_time: datetime
    closing_time: datetime
    status: ScheduleStatusEnum

    @root_validator(pre=True)
    def validate_times(cls, values):
        opening_time = values.get('opening_time')
        closing_time = values.get('closing_time')
        if opening_time and closing_time and closing_time <= opening_time:
            raise ValueError("closing_time must be greater than opening_time")
        return values