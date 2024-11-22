"""
This module defines the PromotionService class which provides various
CRUD (Create, Read, Update, Delete) operations for managing promotions
in a database.

It uses the Peewee ORM for database interaction and FastAPI's HTTPException 
for error handling.

Imports:
    - DoesNotExist, IntegrityError (Peewee exceptions)
    - Body, HTTPException (FastAPI tools)
    - Promotion (Pydantic model for promotion data)
    - PromotionModel (Peewee model for database interaction)
"""

from peewee import DoesNotExist, IntegrityError
from fastapi import HTTPException
from database import PromotionModel
from models.promotion import Promotion, PromotionStatusEnum
from services.user_service import UserService  # Importa el servicio de usuario
from models.person import RoleEnum  # Importa el modelo para la validación del rol
import logging

logger = logging.getLogger(__name__)

class PromotionService:
    """
    Service class for managing promotions.
    """

    @staticmethod
    def get_promotions():
        """
        Retrieve all promotions.

        Returns:
            list: A list of all promotions as dictionaries.
        """
        promotions = PromotionModel.select().dicts()
        return list(promotions)

    @staticmethod
    def get_active_promotions():
        """
        Retrieve all active promotions (AVAILABLE).

        Returns:
            list: A list of active promotions as dictionaries.
        """
        promotions = PromotionModel.select().where(
            PromotionModel.status == PromotionStatusEnum.AVAILABLE.value
        ).dicts()
        return list(promotions)

    @staticmethod
    def get_promotion(promotion_id: int):
        """
        Retrieve a specific promotion by ID.

        Args:
            promotion_id (int): The ID of the promotion.

        Returns:
            dict: The promotion data as a dictionary.

        Raises:
            HTTPException: If the promotion is not found.
        """
        try:
            promotion = PromotionModel.get(PromotionModel.id == promotion_id)
            return promotion.__data__
        except DoesNotExist as exc:
            raise HTTPException(status_code=404, detail="Promotion not found") from exc

    @staticmethod
    def create_promotion(promotion_data: Promotion):
        """
        Create a new promotion.

        Args:
            promotion_data (Promotion): The data for the new promotion.

        Returns:
            dict: The created promotion as a dictionary.

        Raises:
            HTTPException: If the creation fails or validation errors occur.
        """
        # Validación de descuento positivo
        if promotion_data.discount <= 0:
            raise HTTPException(status_code=400, detail="Discount must be greater than zero.")
        
        # Validación de fechas coherentes
        if promotion_data.startTime >= promotion_data.endTime:
            raise HTTPException(status_code=400, detail="Start time must be before end time.")
        
        # Validación del usuario creador (debe ser administrador)
        user = UserService.get_user_by_id(promotion_data.createdBy)
        if not user or user.role != RoleEnum.ADMIN:
            raise HTTPException(status_code=403, detail="Only administrators can create promotions.")
        
        # Validación de descripción no vacía
        if not promotion_data.description.strip():
            raise HTTPException(status_code=400, detail="Description cannot be empty.")

        try:
            new_promotion = PromotionModel.create(
                description=promotion_data.description,
                discount=promotion_data.discount,
                start_time=promotion_data.startTime,
                end_time=promotion_data.endTime,
                status=promotion_data.status.value,
                created_by=promotion_data.createdBy,
            )
            return new_promotion.__data__
        except IntegrityError as exc:
            logger.error(f"Error creating promotion: {exc}")
            raise HTTPException(status_code=400, detail="Error creating promotion") from exc

    @staticmethod
    def update_promotion(promotion_id: int, promotion_data: dict):
        """
        Update an existing promotion.

        Args:
            promotion_id (int): The ID of the promotion to update.
            promotion_data (dict): The updated promotion data.

        Returns:
            dict: The updated promotion as a dictionary.

        Raises:
            HTTPException: If the promotion is not found or the update fails.
        """
        # Validación de descuento positivo
        if promotion_data.get("discount") and promotion_data["discount"] <= 0:
            raise HTTPException(status_code=400, detail="Discount must be greater than zero.")

        # Validación de fechas coherentes
        if promotion_data.get("start_time") and promotion_data.get("end_time"):
            if promotion_data["start_time"] >= promotion_data["end_time"]:
                raise HTTPException(status_code=400, detail="Start time must be before end time.")

        try:
            PromotionModel.update(promotion_data).where(
                PromotionModel.id == promotion_id
            ).execute()
            updated_promotion = PromotionModel.get(PromotionModel.id == promotion_id)
            return updated_promotion.__data__
        except DoesNotExist as exc:
            raise HTTPException(status_code=404, detail="Promotion not found") from exc
        except IntegrityError as exc:
            logger.error(f"Error updating promotion: {exc}")
            raise HTTPException(status_code=400, detail="Error updating promotion") from exc

    @staticmethod
    def delete_promotion(promotion_id: int):
        """
        Delete a promotion by ID.

        Args:
            promotion_id (int): The ID of the promotion to delete.

        Returns:
            str: A success message.

        Raises:
            HTTPException: If the promotion is not found.
        """
        try:
            promotion = PromotionModel.get(PromotionModel.id == promotion_id)
            promotion.delete_instance()
            return "Promotion deleted successfully"
        except DoesNotExist as exc:
            raise HTTPException(status_code=404, detail="Promotion not found") from exc
   