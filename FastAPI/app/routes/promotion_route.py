"""
This module defines the promotion routes for the FastAPI application.

The routes include endpoints for creating, retrieving, updating, and deleting promotions.

### Routes:
- `GET /`: Retrieves a list of all promotions.
- `GET /{promotion_id}`: Retrieves a specific promotion by its ID.
- `POST /`: Creates a new promotion in the application.
- `PUT /{promotion_id}`: Updates an existing promotion by its ID.
- `DELETE /{promotion_id}`: Deletes a promotion by its ID.

### Dependencies:
- `PromotionService`: A service class responsible for promotion operations.

### Models:
- `Promotion`: Represents the promotion data model.
"""
from peewee import DoesNotExist, IntegrityError
from fastapi import HTTPException
from database import PromotionModel
from models.promotion import Promotion
from fastapi import APIRouter, Body, Depends
from helpers.api_key_auth import admin_required  
from services.promotion_service import PromotionService  # Importa el servicio de promociones


promotion_route = APIRouter()

@promotion_route.get("/", dependencies=[Depends(admin_required)])
def get_promotions():
    """
    Retrieves all promotions from the database.
    
    ### Returns:
    - List of all promotions as dictionaries.
    """
    return PromotionService.get_promotions()


@promotion_route.get("/active", dependencies=[Depends(admin_required)])
def get_active_promotions():
    """
    Retrieve all active promotions (only those with status 'AVAILABLE').
    
    ### Returns:
    - List of active promotions as dictionaries.
    """
    return PromotionService.get_active_promotions()


@promotion_route.get("/{promotion_id}")
def get_promotion(promotion_id: int):
    """
    Retrieves a specific promotion by its ID.
    
    ### Args:
    - promotion_id (int): The ID of the promotion to retrieve.
    
    ### Returns:
    - Promotion: The promotion data for the given ID.
    
    ### Raises:
    - HTTPException: If the promotion is not found in the database.
    """
    return PromotionService.get_promotion(promotion_id)


@promotion_route.post("/")
def create_promotion(promotion: Promotion = Body(...)):
    """
    Create a new promotion in the database.
    
    ### Args:
    - promotion (Promotion): A Pydantic model instance representing the new promotion data.
    
    ### Returns:
    - Promotion: The created promotion object.
    
    ### Raises:
    - HTTPException: If any validation fails or the promotion already exists.
    """
    return PromotionService.create_promotion(promotion)


@promotion_route.put("/{promotion_id}")
def update_promotion(promotion_id: int, promotion: Promotion = Body(...)):
    """
    Updates an existing promotion by its ID.
    
    ### Args:
    - promotion_id (int): The ID of the promotion to update.
    - promotion (Promotion): The updated promotion data.
    
    ### Returns:
    - Promotion: The updated promotion object.
    
    ### Raises:
    - HTTPException: If the promotion is not found or the update fails.
    """
    return PromotionService.update_promotion(promotion_id, promotion.dict())


@promotion_route.delete("/{promotion_id}")
def delete_promotion(promotion_id: int):
    """
    Delete a promotion by its ID.
    
    ### Args:
    - promotion_id (int): The ID of the promotion to delete.
    
    ### Returns:
    - str: A success message if the promotion is deleted successfully.
    
    ### Raises:
    - HTTPException: If the promotion is not found in the database.
    """
    return PromotionService.delete_promotion(promotion_id)


@promotion_route.get("/user/{user_id}")
def get_user_promotions(user_id: int):
    """
    Retrieve all promotions created by a specific user (typically an admin).
    
    ### Args:
    - user_id (int): The ID of the user whose promotions are being retrieved.
    
    ### Returns:
    - List of promotions created by the user.
    
    ### Raises:
    - HTTPException: If the user has no promotions or there is an error.
    """
    # This route can be useful to allow the admin to see the promotions they've created.
    user_promotions = PromotionService.get_promotions_by_user(user_id)
    if not user_promotions:
        raise HTTPException(status_code=404, detail="No promotions found for this user.")
    return user_promotions
