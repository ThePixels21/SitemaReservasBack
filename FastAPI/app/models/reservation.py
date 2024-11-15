"""
This module defines the `Reservation` model and the `ReservationStatusEnum` enumeration.

The `Reservation` model includes attributes such as ID, user who reserved, workspace reserved,
start and end times, status, and price.

Classes:
    ReservationStatusEnum: Enumeration for the status of a reservation.
    Reservation: Represents a reservation with various attributes.
"""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class ReservationStatusEnum(str, Enum):
    """
    Enumeration for the status of a reservation.

    Attributes:
        ACTIVE (str): Indicates the reservation is currently active.
        CANCELLED (str): Indicates the reservation has been cancelled.
    """
    ACTIVE = "Active"
    CANCELLED = "Cancelled"

class Reservation(BaseModel):
    """
    Represents a reservation with details such as the user who reserved,
    the workspace reserved, start and end times, status, and price.

    Attributes:
        id (int): The unique identifier for the reservation.
        reservedBy (User): The user who made the reservation.
        workspace (Workspace): The workspace that is reserved.
        startTime (datetime): The start time of the reservation.
        endTime (datetime): The end time of the reservation.
        status (ReservationStatusEnum): The current status of the reservation.
        price (float): The price of the reservation.
    """
    reservedBy: int
    workspace: int
    startTime: datetime
    endTime: datetime = None
    cancelledAt: datetime = None
    status: ReservationStatusEnum
    price: float
