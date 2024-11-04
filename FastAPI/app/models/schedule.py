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
from pydantic.v1.class_validators import Validator, validator


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

    @validator('closing_time')
    def closing_time_must_be_later(cls, closing_time, values):
        """Validates that closing_time is after opening_time."""
        opening_time = values.get('opening_time')
        if opening_time and closing_time <= opening_time:
            raise ValueError('closing_time must be later than opening_time')
        return closing_time