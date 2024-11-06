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
        openingTime (datetime): The opening time of the schedule.
        closingTime (datetime): The closing time of the schedule.
        status (ScheduleStatusEnum): The current status of the schedule.
    """

    id: int
    openingTime: datetime
    closingTime: datetime
    status: ScheduleStatusEnum
