"""
This module provides authentication services for the FastAPI application.

It includes functions for user authentication, password hashing, token generation, 
and user verification using JWT (JSON Web Tokens).

### Functions:

- `verify_password(plain_password, password)`: 
  Verifies a plain password against a hashed password.
  
- `get_password_hash(password)`: 
  Hashes a plain password.

- `get_user(email: str)`: 
  Retrieves a user by their email address.

- `authenticate_user(email: str, password: str)`: 
  Authenticates a user based on their email and password.

- `create_access_token(data: dict, expires_delta: Optional[timedelta] = None)`: 
  Creates a JWT access token with an expiration time.

- `generate_token(email, password)`: 
  Generates an access token for the authenticated user.

- `get_current_user(token: str)`: 
  Retrieves the current user from the access token.

### Dependencies:
- `fastapi`: Web framework for building APIs.
- `jose`: Library for encoding and decoding JSON Web Tokens.
- `passlib`: Library for password hashing.
- `models.token_schema`: Contains the data model for token data.
- `database`: Contains configuration for database connection and secret keys.

"""
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt
from passlib.context import CryptContext

from models.token_schema import TokenData
from database import secret_key, token_expire, PersonModel

SECRET_KEY = secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = token_expire

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")

def verify_password(plain_password, password):
    """
    Verifies a plain password against a hashed password.

    ### Args
    - plain_password (str): The plain text password.
    - password (str): The hashed password to verify against.

    ### Returns
    - bool: True if the passwords match, otherwise False.
    """
    return pwd_context.verify(plain_password, password)

def get_password_hash(password):
    """
    Hashes a plain password.

    ### Args
    - password (str): The plain text password to hash.

    ### Returns
    - str: The hashed password.
    """
    return pwd_context.hash(password)

def get_user(email: str):
    """
    Retrieves a user by their email address.

    ### Args
    - email (str): The email address of the user.

    ### Returns
    - PersonModel: The user object if found, otherwise None.
    """
    return PersonModel.filter(
        (PersonModel.email == email) |
        (PersonModel.email == email)
    ).first()

def authenticate_user(email: str, password: str):
    """
    Authenticates a user based on their email and password.

    ### Args
    - email (str): The user's email address.
    - password (str): The user's password.

    ### Returns
    - PersonModel: The authenticated user object if successful, 
      otherwise False.
    """
    user = get_user(email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict,
                        expires_delta: Optional[timedelta] = None):
    """
    Creates a JWT access token with an expiration time.

    ### Args
    - data (dict): The data to encode in the token.
    - expires_delta (Optional[timedelta]): The expiration time 
      for the token.

    ### Returns
    - str: The encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,
                              SECRET_KEY,
                              algorithm=ALGORITHM)
    return encoded_jwt

def generate_token(email, password):
    """
    Generates an access token for the authenticated user.

    ### Args
    - email (str): The user's email address.
    - password (str): The user's password.

    ### Returns
    - str: The generated access token.

    ### Raises
    - HTTPException: If authentication fails.
    """
    user = authenticate_user(email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Retrieves the current user from the access token.

    ### Args
    - token (str): The access token.

    ### Returns
    - PersonModel: The current user object.

    ### Raises
    - HTTPException: If token validation fails.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError as exc:
        raise credentials_exception from exc

    user = get_user(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user
