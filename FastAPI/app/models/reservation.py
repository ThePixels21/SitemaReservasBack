from datetime import datetime
from enum import Enum

from pydantic import BaseModel

from FastAPI.app.models.person import User
from FastAPI.app.models.workspace import Workspace


class ReservationStatusEnum(str, Enum):
    ACTIVE = "Active"
    CANCELLED = "Cancelled"

class Reservation(BaseModel):
    id: int
    reservedBy: User
    workspace: Workspace
    startTime: datetime
    endTime: datetime
    status: ReservationStatusEnum
    price: float