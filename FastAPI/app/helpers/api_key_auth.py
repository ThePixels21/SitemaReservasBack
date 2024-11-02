"""
This module handles API key authentication to protect FastAPI application endpoints.
It uses a header-based authentication scheme, where the client is expected to send
the API key in the 'x-api-key' HTTP header. If the key is valid, access is granted;
otherwise, a 403 (Forbidden) exception is raised.
"""

import os
from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from dotenv import load_dotenv

from FastAPI.app.database import PersonModel
from FastAPI.app.models.person import RoleEnum

# Load environment variables
load_dotenv()

# Configuration variables
API_KEY = os.getenv("API_KEY")
API_KEY_NAME = "x-api-key"

# Define the API key header scheme
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    """
    Verifies if the API key provided in the headers matches the expected key.

    :param api_key: API key extracted from the HTTP headers.
    :return: The API key if it matches.
    :raises HTTPException: If the API key does not match, a 403 (Forbidden) exception is raised.
    """
    if api_key == API_KEY:
        return api_key

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail={
            "status": False,
            "status_code": status.HTTP_403_FORBIDDEN,
            "message": "Unauthorized",
        },
    )


def admin_required(user_id: int):
    """
    Verifies if the user has an admin role. Only admins can proceed.

    :param user_id: ID of the current user.
    :return: The PersonModel instance if the user is an admin.
    :raises HTTPException: If the user is not an admin.
    """
    user = PersonModel.get_or_none(PersonModel.id == user_id)
    if user is None or user.role != RoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required."
        )
    return user
