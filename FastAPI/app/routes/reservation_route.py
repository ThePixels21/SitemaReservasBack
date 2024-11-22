"""
Reservation Route Module.

This module defines the FastAPI routes for managing reservations in a workspace booking system.
It includes endpoints to create, update, retrieve, and delete reservations, as well as retrieve 
reservations based on specific criteria, such as user ID or cancellation status.

Dependencies:
    - APIRouter (FastAPI): Provides routing functionality for the reservation API endpoints.
    - admin_required, user_required: Dependency functions to enforce role-based access control.
    - ReservationService: Service class that handles business logic for reservations.
    - ReservationModel: The database model for reservations.
"""
from fastapi import APIRouter, Body, Depends

from helpers.api_key_auth import admin_required
from models.reservation import Reservation
from services.reservation_service import ReservationService

reservation_route = APIRouter()


@reservation_route.get("/",dependencies=[Depends(admin_required)])
def get_reservations():
    """
    Retrieves all reservations from the database.

    ### Returns
    - List[ReservationModel]: A list of all reservations.
    """
    return ReservationService.get_reservations()

@reservation_route.get("/{reservation_id}")
def get_reservation(reservation_id: int):
    """
    Retrieves a reservation by its ID.

    ### Args
    - reservation_id (int): The unique identifier of the reservation.

    ### Returns
    - ReservationModel: The reservation object if found.

    ### Raises
    - HTTPException: If the reservation is not found in the database.
    """
    return ReservationService.get_reservation(reservation_id)

@reservation_route.post("/")
def create_reservation(reservation: Reservation = Body(...)):
    """
    Creates a new reservation in the database.

    ### Args
    reservation (ReservationModel): A Pydantic model instance representing the new reservation data.

    ### Returns
    - ReservationModel: The created reservation object.

    ### Raises
    - HTTPException: If any validation fails or the reservation already exists.
    """
    return ReservationService.create_reservation(reservation)

@reservation_route.post("/with-promotion/")
def create_reservation_with_promotion(
    reservation: Reservation = Body(...), 
    apply_promotion: bool = Body(False)
):
    """
    Create a reservation and optionally apply a promotion.

    ### Args
    - reservation (Reservation): Reservation details.
    - apply_promotion (bool): Whether to apply a promotion.

    ### Returns
    - ReservationModel: The created reservation.
    """
    return ReservationService.create_reservation_with_promotion(reservation, apply_promotion)

@reservation_route.put("/{reservation_id}")
def update_reservation(reservation_id: int, reservation: Reservation = Body(...)):
    """
    Updates an existing reservation by its ID.

    ### Args
    - reservation_id (int): The unique identifier of the reservation.
    reservation (ReservationModel): A Pydantic model instance representing the updated data.

    ### Returns
    - ReservationModel: The updated reservation object.

    ### Raises
    - HTTPException: If the reservation is not found or the update fails.
    """
    return ReservationService.update_reservation(reservation_id, reservation)

@reservation_route.delete("/{reservation_id}")
def delete_reservation(reservation_id: int):
    """
    Deletes a reservation by its ID.

    ### Args
    - reservation_id (int): The unique identifier of the reservation.

    ### Returns
    - dict: A success message if the reservation is deleted.

    ### Raises
    - HTTPException: If the reservation is not found in the database.
    """
    return ReservationService.delete_reservation(reservation_id)

@reservation_route.get("/user/{user_id}")
def get_all_reservation_user(user_id: int):
    """
    Retrieves all reservations made by a specific user.

    ### Args
    - user_id (int): The unique identifier of the user.

    ### Returns
    - List[ReservationModel]: A list of reservations associated with the specified user.

    ### Raises
    - HTTPException: If no reservations are found for the user.
    """
    return ReservationService.get_all_reservation_user(user_id)

@reservation_route.get("/cancel", dependencies=[Depends(admin_required)])
def get_all_reservation_cancel():
    """
    Retrieves all reservations with a CANCELLED status.

    ### Returns
    - List[ReservationModel]: A list of cancelled reservations.
    """
    return ReservationService.get_all_reservation_cancel()
