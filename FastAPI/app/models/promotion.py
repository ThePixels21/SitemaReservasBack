from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class PromotionStatusEnum(str, Enum):
    AVAILABLE = "Available"
    FINISHED = "Finished"


class Promotion(BaseModel):
    id: int
    description: str
    discount: float
    startTime: datetime
    endTime: datetime
    status: PromotionStatusEnum
    reservation: Optional["Reservation"]
    createdBy: str