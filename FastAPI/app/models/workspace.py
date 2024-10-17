from enum import Enum

from pydantic import BaseModel

from FastAPI.app.models.person import User


class WorkspaceEnum(str, Enum):
    OFFICE = "Office"
    MEETING_ROOM = "MeetingRoom"
    DESK = "Desk"

class Workspace(BaseModel):
    id: int
    type: WorkspaceEnum
    capacity: int
    hourlyRate: float
    availableSchedules: list
    createdBy: str