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
