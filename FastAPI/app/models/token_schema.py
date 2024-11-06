"""
This module defines two data models: Token and TokenData.

Classes:
    Token: Represents a token used for authentication.
    TokenData: Represents additional data associated with a token, such as a email.
"""
from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    """
    Represents a token used for authentication.

    Attributes:
    access_token (str): The token used to access resources.
    token_type (str): The type of the token (e.g., Bearer).
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Represents data related to the token, including optional user information.

    Attributes:
    email (Optional[str]): The email associated with the token, if available.
    """
    email: Optional[str] = None
