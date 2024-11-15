"""
This module defines the `Promotion` model and its associated
enumeration `PromotionStatusEnum`.

The `Promotion` model includes details such as description, discount,
 start and end times, status, reservation, and creator.

Classes:
    PromotionStatusEnum: Enumeration for the status of a promotion.
    Promotion: Represents a promotion with various attributes.

Attributes:
    id (int): The unique identifier for the promotion.
    description (str): A brief description of the promotion.
    discount (float): The discount percentage offered by the promotion.
    startTime (datetime): The start time of the promotion.
    endTime (datetime): The end time of the promotion.
    status (PromotionStatusEnum): The current status of the promotion.
    reservation (Optional[Reservation]): The reservation associated with the promotion, if any.
    createdBy (str): The user who created the promotion.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from .reservation import Reservation


class PromotionStatusEnum(str, Enum):
    """
    Enumeration for the status of a promotion.

    Attributes:
        AVAILABLE (str): Indicates the promotion is currently available.
        FINISHED (str): Indicates the promotion has finished.
    """
    AVAILABLE = "Available"
    FINISHED = "Finished"


class Promotion(BaseModel):
    """
    Represents a promotion with details such as description, discount,
    start and end times, status, reservation, and creator.

    Attributes:
        id (int): The unique identifier for the promotion.
        description (str): A brief description of the promotion.
        discount (float): The discount percentage offered by the promotion.
        startTime (datetime): The start time of the promotion.
        endTime (datetime): The end time of the promotion.
        status (PromotionStatusEnum): The current status of the promotion.
        reservation (Optional[Reservation]): The reservation associated with the promotion, if any.
        createdBy (str): The user who created the promotion.
    """
    description: str
    discount: float
    startTime: datetime
    endTime: datetime
    status: PromotionStatusEnum
    reservation: Optional["Reservation"]
    createdBy: str
