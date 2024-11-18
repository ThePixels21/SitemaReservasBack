"""
This module defines the UserService class which provides various
CRUD (Create, Read, Update, Delete) operations for managing users 
in a database.

It uses the Peewee ORM for database interaction and FastAPI's HTTPException 
for error handling. The operations include retrieving all users, creating 
new users with validation, updating user details, and deleting users.

Imports:
    - DoesNotExist, IntegrityError (Peewee exceptions)
    - Body, HTTPException (FastAPI tools)
    - User (Pydantic model for user data)
    - UserModel (Peewee model for database interaction)
"""

import re
from peewee import DoesNotExist, IntegrityError

from models.person import User
from database import PersonModel
from fastapi import Body, HTTPException
from services.auth_service import get_password_hash,get_current_user


class UserService:
    """
    A service class that provides user-related operations such as 
    retrieving, creating, updating, and deleting users in the database.

    This class interacts with the database through the `UserModel` to 
    manage user data, while also enforcing validation rules for passwords
    and ensuring user uniqueness.
    """

    @staticmethod
    def get_users():
        """
        Retrieve all users from the database.

        Returns:
            List[UserModel]: A list of all users.
        """
        users = list(PersonModel.select)
        return users

    @staticmethod
    def get_user(user_id: int):
        """
        Retrieve a user by their ID.

        Args:
            id (int): The ID of the user to retrieve.

        Returns:
            UserModel: The user object if found.

        Raises:
            HTTPException: If the user is not found in the database.
        """
        try:
            user = PersonModel.get(PersonModel.id == user_id)
            return user
        except DoesNotExist as exc:
            raise HTTPException(status_code=404, detail="User not found") from exc

    @staticmethod
    async def get_user_by_token(token: str):
        """
        Retrieve the user by their access token.
        """
        user = await get_current_user(token)

        if user is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return user

    @staticmethod
    def create_user(user: User = Body(...)):
        """
        Create a new user in the database with validation.

        Args:
            user (User): A Pydantic model instance representing the new user data.

        Returns:
            UserModel: The created user object.

        Raises:
            HTTPException: If any validation fails or the user already exists.
        """
        # Password validation
        if len(user.password) < 8:
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters")

        if not any(char.isdigit() for char in user.password):
            raise HTTPException(status_code=400, detail="Password must contain at least one number")

        if not any(char.isalpha() for char in user.password):
            raise HTTPException(status_code=400, detail="Password must contain at least one letter")

        if not any(char in '@$!%*?&' for char in user.password):
            raise HTTPException(status_code=400, detail="Password must contain a special character")

        try:
            if not all([user.name, user.email, user.password, user.role]):
                raise HTTPException(status_code=400, detail="Missing required fields")
            # Patrón actualizado para permitir los dominios especificados
            pattern = r'^[a-zA-Z0-9.-]+@(gmail\.(com|co|com\.co)|eam\.edu\.co)$'
            if re.match(pattern, user.email) is None:
                raise HTTPException(status_code=400,detail="Use a valid characters")
            for existing_user in PersonModel.select():
                if existing_user.email == user.email:
                    raise HTTPException(status_code=400, detail="User already exists")

            if "@" not in user.email or not user.email.split('@')[-1]:
                raise HTTPException(status_code=400,
                detail="Email must contain an '@' and a domain (e.g., '@gmail.com')"
                )
            # Create the user
            created_user = PersonModel.create(
                name=user.name,
                email=user.email,
                password=get_password_hash(user.password),
                role=user.role
            )
            return created_user

        except IntegrityError as exc:
            raise HTTPException(status_code=400, detail="User already exists") from exc

    @staticmethod
    def update_user(user_id: int, user: User = Body(...)):
        """
        Update an existing user's information in the database.

        Args:
            id (int): The ID of the user to update.
            user (User): A Pydantic model instance representing the updated user data.

        Returns:
            UserModel: The updated user.

        Raises:
            HTTPException: If the user is not found or the update fails.
        """
        try:
            # Find the user to update
            existing_user = PersonModel.get(PersonModel.id == user_id)

            # Password validation if it is to be updated
            if user.email is None or user.password is None or user.role is None:
                raise HTTPException(status_code=400, detail="Missing required fields")
            if user.password and len(user.password) < 8 or user.name is None:
                raise HTTPException(
                    status_code=400, detail="Password must be at least 8 characters"
                    )

            if user.password and not any(char.isdigit() for char in user.password):
                raise HTTPException(
                    status_code=400, detail="Password must contain at least one number"
                    )
            if user.password and not any(char.isalpha() for char in user.password):
                raise HTTPException(
                    status_code=400, detail="Password must contain at least one letter"
                    )

            if user.password and not any(char in '@$!%*?&' for char in user.password):
                raise HTTPException(
                    status_code=400, detail="Password must contain a special character"
                    )

            if "@" not in user.email or not user.email.split('@')[-1]:
                raise HTTPException(status_code=400,
                detail="Email must contain an '@' and a domain (e.g., '@gmail.com')")

            # Check if another user with the same email already exists
            for existing_user in PersonModel.select():
                if existing_user.email == user.email:
                    raise HTTPException(status_code=400, detail="User already exists")

            # Update the user's information
            existing_user.name = user.name or existing_user.name
            existing_user.email = user.email or existing_user.email
            existing_user.password = get_password_hash(user.password) or existing_user.password
            existing_user.role = user.role or existing_user.role

            # Save changes to the database
            existing_user.save()
            return existing_user

        except DoesNotExist as exc:
            raise HTTPException(status_code=404, detail="User not found") from exc
        except IntegrityError as exc:
            raise HTTPException(status_code=400, detail="Could not update user") from exc

    @staticmethod
    def delete_user(user_id: int):
        """
        Delete a user from the database by their ID.

        Args:
            id (int): The ID of the user to delete.

        Returns:
            dict: A success message if the user is deleted.

        Raises:
            HTTPException: If the user is not found in the database.
        """
        try:
            person = PersonModel.get(PersonModel.id == user_id)
            person.delete_instance()
            return {"status": "User deleted successfully"}
        except DoesNotExist as exc:
            raise HTTPException(status_code=404, detail="User not found") from exc