"""
This module defines the user routes for the FastAPI application.

The routes include endpoints for creating, retrieving, updating, and deleting users,
as well as a login endpoint for obtaining an access token.

### Routes:
- `GET /`: Retrieves a list of all users.
- `GET /{user_id}`: Retrieves a specific user by their ID.
- `POST /`: Creates a new user in the application.
- `PUT /{user_id}`: Updates an existing user by their ID.
- `DELETE /{user_id}`: Deletes a user by their ID.
- `POST /login`: Logs in a user and returns an access token.

### Dependencies:
- `UserService`: A service class responsible for user operations.
- `generate_token`: A function that generates a token for authentication.

### Models:
- `User`: Represents the user data model.
- `Token`: Represents the token schema returned after successful login.
"""

# Third-party imports
from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm

# Local application/library specific imports
from models.person import User
from models.token_schema import Token
from services.auth_service import generate_token
from services.user_service import UserService

user_route = APIRouter()

@user_route.get("/")
def get_user():
    """
    Retrieves a list of all users.

    ### Returns
    - List of users.
    """
    return UserService.get_users()

@user_route.get("/{user_id}")
def get_user_by_id(user_id: int):
    """
    Retrieves a specific user by their ID.

    ### Args
    - user_id (int): The unique identifier of the user.

    ### Returns
    - User: The user information corresponding to the provided ID.
    """
    return UserService.get_user(user_id)

@user_route.post("/")
def create_user(user: User = Body(...)):
    """
    Create a new user in the app.

    ### Args
    The app can receive the following fields in a JSON body:
    - email: A valid email address.
    - username: A unique username.
    - password: A strong password for authentication.

    ### Returns
    - User: Information of the created user.
    """
    return UserService.create_user(user)

@user_route.put("/{user_id}")
def update_user(user_id: int, user: User = Body(...)):
    """
    Updates an existing user by their ID.

    ### Args
    - user_id (int): The unique identifier of the user.
    - user (User): The user data to update.

    ### Returns
    - User: The updated user information.
    """
    return UserService.update_user(user_id, user)

@user_route.delete("/{user_id}")
def delete_user(user_id: int):
    """
    Deletes a user by their ID.

    ### Args
    - user_id (int): The unique identifier of the user.

    ### Returns
    - None: Confirmation of deletion.
    """
    return UserService.delete_user(user_id)

@user_route.post(
    "/login",
    response_model=Token
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Logs in a user and returns an access token.

    ### Args
    The app can receive the following fields by form data:
    - username: Your username or email.
    - password: Your password.

    ### Returns
    - Token: Contains the access token and token type.
    """
    access_token = generate_token(form_data.username, form_data.password)
    return Token(access_token=access_token, token_type="bearer")
