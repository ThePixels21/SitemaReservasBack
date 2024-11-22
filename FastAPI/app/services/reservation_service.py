"""
Reservation Service Module.

This module defines the `ReservationService` class, which provides methods to manage reservations
in a workspace booking system. It includes functionality for creating, updating, retrieving, and 
deleting reservations, with specific validations based on reservation status, 
user roles, and workspace 
capacity constraints.

Classes:
    ReservationService: A service class containing static methods to handle all 
    reservation operations.

Exceptions:
    HTTPException: Raised when operations fail, such as if a reservation is not found or 
    validation errors occured.

Dependencies:
    peewee.DoesNotExist, peewee.IntegrityError
    fastapi.Body, fastapi.HTTPException
    models.reservation.ReservationStatusEnum
    models.workspace.Workspace
    models.person.User
    database.ReservationModel
"""
from datetime import datetime
from peewee import DoesNotExist, IntegrityError
from fastapi import Body, HTTPException

from models.promotion import PromotionStatusEnum
from models.reservation import ReservationStatusEnum
from models.person import RoleEnum
from database import ReservationModel
from services.user_service import UserService
from services.workspace_service import WorkspaceService
from models.reservation import Reservation 
from models.promotion import Promotion 


class ReservationService:
    """
    A service class for managing reservation operations. This class provides methods 
    for creating, updating, retrieving, and deleting reservations, as well as managing 
    reservation-related business rules and validations.
    """
    @staticmethod
    def get_reservations():
        """
        Retrieve all reservations from the database.

        Returns:
            list: A list of all reservations.
        """
        reservations = list(ReservationModel.select())
        return reservations

    @staticmethod
    def get_reservation(reservation_id: int):
        """
        Retrieve a reservation by its ID.

        Args:
            reservation_id (int): The ID of the reservation to retrieve.

        Returns:
            ReservationModel: The reservation instance if found.

        Raises:
            HTTPException: If the reservation is not found.
        """
        try:
            reservation = ReservationModel.get(ReservationModel.id == reservation_id)
            return reservation
        except DoesNotExist as exc:
            raise HTTPException(status_code=404, detail="User not found") from exc

    @staticmethod
    def get_all_reservation_user(user_id: int):
        """
        Retrieve all reservations for a specific user.

        Args:
            user_id (int): The ID of the user whose reservations are being retrieved.

        Returns:
            list: A list of reservations associated with the specified user.

        Raises:
            HTTPException: If no reservations are found for the user.
        """
        try:
            reservations = list(
                ReservationModel.select().where(ReservationModel.reservedBy == user_id)
                )
            return reservations
        except DoesNotExist as exc:
            raise HTTPException(status_code=404, detail="User not found") from exc

    @staticmethod
    def create_reservation(reservation: ReservationModel = Body(...)):
        """
        Create a new reservation.

        Args:
            workspace (Workspace): The workspace associated with the reservation.
            reservation (ReservationModel): The reservation details.

        Returns:
            ReservationModel: The created reservation instance.

        Raises:
            HTTPException: If validation fails or the reservation already exists.
        """
        user = UserService.get_user(reservation.reservedBy)
        workspace = WorkspaceService.get_workspace(reservation.workspace)
        if user is None:
            raise HTTPException(status_code=400,detail="Only need valid user ")
        if workspace is None:
            raise HTTPException(status_code=400,detail="Only need valid workspace")
        if user.role != RoleEnum.USER:
            raise HTTPException(status_code=400, detail="Only users can reserve workspaces")
        if reservation.startTime > reservation.endTime:
            raise HTTPException(status_code=400, detail="Start time must be before end time")
        if reservation.status != ReservationStatusEnum.ACTIVE:
            raise HTTPException(status_code=400, detail="Reservation status must be active")
        if reservation.price < 0:
            raise HTTPException(status_code=400, detail="Reservation price must be positive")
        try:
            print(user,workspace)
            print("Entra")
            reservation = ReservationModel.create(
                reservedBy=user,
                workspace=workspace,
                startTime=reservation.startTime,
                endTime=reservation.endTime,
                status=ReservationStatusEnum.ACTIVE,
                price=reservation.price
            )
            print("Entra2")
            return reservation
        except IntegrityError as exc:
            raise HTTPException(status_code=400, detail="Reservation already exists") from exc



    @staticmethod
    def update_reservation(reservation_id: int, reservation: ReservationModel = Body(...)):
        """
        Update an existing reservation.

        Args:
            reservation_id (int): The ID of the reservation to update.
            reservation (ReservationModel): The updated reservation details.

        Returns:
            ReservationModel: The updated reservation instance.

        Raises:
            HTTPException: If validation fails, reservation is not found, or update fails.
        """
        try:
            reservation = ReservationModel.get(ReservationModel.id == reservation_id)
            if reservation.reservedBy.role != RoleEnum.USER:
                raise HTTPException(status_code=400, detail="Only users can reserve workspaces")
            if reservation.startTime > reservation.endTime:
                raise HTTPException(status_code=400,
                    detail="Start time must be before end time")
            if reservation.status != ReservationStatusEnum.ACTIVE:
                raise HTTPException(status_code=400, detail="Reservation status must be active")
            if reservation.price < 0:
                raise HTTPException(status_code=400, detail="Reservation price must be positive")
            if reservation.workspace.capacity < 1:
                raise HTTPException(status_code=400,
                    detail="Workspace capacity must be greater than 0")
            if reservation.workspace.capacity <= reservation.workspace.capacity:
                raise HTTPException(status_code=400,
                    detail="Workspace capacity must be greater than reservation capacity")
            reservation.reservedBy = reservation.reservedBy
            reservation.workspace = reservation.workspace
            reservation.startTime = reservation.startTime
            reservation.endTime = reservation.endTime
            reservation.status = ReservationStatusEnum.ACTIVE
            reservation.price = reservation.price
            reservation.save()
            return reservation
        except DoesNotExist as exc:
            raise HTTPException(status_code=404, detail="Reservation not found") from exc
        except IntegrityError as exc:
            raise HTTPException(status_code=400, detail="Could not update reservation") from exc

    @staticmethod
    def delete_reservation(reservation_id: int):
        """
        Delete a reservation by setting its status to CANCELLED.

        Args:
            reservation_id (int): The ID of the reservation to delete.

        Returns:
            dict: A dictionary confirming deletion.

        Raises:
            HTTPException: If the reservation is not found.
        """
        try:
            reservation = ReservationModel.get(ReservationModel.id == reservation_id)
            reservation.status = ReservationStatusEnum.CANCELLED
            reservation.cancelledAt = datetime.now()
            reservation.save()
            return {"status": "Reservation deleted successfully"}
        except DoesNotExist as exc:
            raise HTTPException(status_code=404, detail="Reservation not found") from exc

    @staticmethod
    def get_all_reservation_cancel():
        """
        Retrieve all reservations with a CANCELLED status.

        Returns:
            list: A list of cancelled reservations.
        """
        reservation = list(
            ReservationModel.select().where(
                ReservationModel.status == ReservationStatusEnum.CANCELLED))
        return reservation
    
    @staticmethod
    def create_reservation_with_promotion(reservation: Reservation, apply_promotion: bool = False):
        """
        Create a reservation and optionally apply a promotion.

        Args:
            reservation (Reservation): The reservation details.
            apply_promotion (bool): Whether to apply a promotion.

        Returns:
            ReservationModel: The created reservation.

        Raises:
            HTTPException: If validation fails or the reservation already exists.
        """
      
        user = UserService.get_user(reservation.reservedBy)
        workspace = WorkspaceService.get_workspace(reservation.workspace)
        if user is None:
            raise HTTPException(status_code=400, detail="Only need valid user")
        if workspace is None:
            raise HTTPException(status_code=400, detail="Only need valid workspace")
        if user.role != RoleEnum.USER:
            raise HTTPException(status_code=400, detail="Only users can reserve workspaces")
        if reservation.startTime > reservation.endTime:
            raise HTTPException(status_code=400, detail="Start time must be before end time")
        if reservation.status != ReservationStatusEnum.ACTIVE:
            raise HTTPException(status_code=400, detail="Reservation status must be active")
        if reservation.price < 0:
            raise HTTPException(status_code=400, detail="Reservation price must be positive")

        promotion_details = None
        
        if apply_promotion:
            promotion = Promotion.select().where(
                (Promotion.status == PromotionStatusEnum.AVAILABLE) & 
                (Promotion.startTime <= reservation.startTime) & 
                (Promotion.endTime >= reservation.endTime)
            ).first()

            if promotion:
                # Validar condiciones de la promoción
                if reservation.endTime - reservation.startTime >= promotion.minDuration:
                    if reservation.startTime.weekday() in [day.value for day in promotion.applicableDays]:
                        discount = promotion.discount
                        reservation.price -= reservation.price * (discount / 100) if promotion.discountType == "percent" else discount

                        # Evitar precios negativos
                        if reservation.price < 0:
                            reservation.price = 0
                        promotion_details = {
                            "description": promotion.description,
                            "discount": promotion.discount,
                            "discount_type": promotion.discountType
                        }
                else:
                    raise HTTPException(status_code=400, detail="Reservation does not meet promotion conditions")

        try:
            created_reservation = ReservationModel.create(
                reservedBy=user,
                workspace=workspace,
                startTime=reservation.startTime,
                endTime=reservation.endTime,
                status=ReservationStatusEnum.ACTIVE,
                price=reservation.price
            )
            return {
                "reservation": created_reservation,
                "promotion_details": promotion_details
            }
        except IntegrityError as exc:
            raise HTTPException(status_code=400, detail="Reservation already exists") from exc

