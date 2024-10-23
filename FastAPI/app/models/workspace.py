"""
This module defines the `Workspace` model and the `WorkspaceEnum` enumeration.

The `Workspace` model includes attributes such as ID, type, capacity, hourly rate,
available schedules, and the user who created it.

Classes:
    WorkspaceEnum: Enumeration for the type of workspace.
    Workspace: Represents a workspace with various attributes.
"""
from enum import Enum

from pydantic import BaseModel

class WorkspaceEnum(str, Enum):
    """
    Enumeration for the type of a workspace.

    Attributes:
        OFFICE (str): Indicates the workspace is an office.
        MEETING_ROOM (str): Indicates the workspace is a meeting room.
        DESK (str): Indicates the workspace is a desk.
    """
    OFFICE = "Office"
    MEETING_ROOM = "MeetingRoom"
    DESK = "Desk"

class Workspace(BaseModel):
    """
    Represents a workspace with details such as type, capacity, hourly rate,
    available schedules, and the user who created it.

    Attributes:
        id (int): The unique identifier for the workspace.
        type (WorkspaceEnum): The type of the workspace (e.g., Office, Meeting Room, Desk).
        capacity (int): The capacity of the workspace.
        hourlyRate (float): The hourly rate for reserving the workspace.
        availableSchedules (list): A list of available schedules for the workspace.
        createdBy (str): The user who created the workspace.
    """
    id: int
    type: WorkspaceEnum
    capacity: int
    hourlyRate: float
    availableSchedules: list
    createdBy: str
