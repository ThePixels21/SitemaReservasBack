"""
This module defines the `Person`, `User`, and `Admin` models along with the `RoleEnum` enumeration.

The `Person` model includes attributes such as ID, name, email, password, and role.
The `User` and `Admin` models inherit from the `Person` model and represent specific
 types of persons with roles 'User' and 'Admin' respectively.

Classes:
    RoleEnum: Enumeration for the role of a person.
    Person: Represents a person with various attributes.
    User: Represents a user who inherits from the Person class.
    Admin: Represents an admin who inherits from the Person class.
"""
from enum import Enum

from pydantic import BaseModel

class RoleEnum(str, Enum):
    """
    Enumeration for the role of a person.

    Attributes:
        ADMIN (str): Indicates the person has an admin role.
        USER (str): Indicates the person has a user role.
    """
    ADMIN = "Admin"
    USER = "User"

class Person(BaseModel):
    """
    Represents a person with attributes such as ID, name, email, password, and role.

    Attributes:
        id (int): The unique identifier for the person.
        name (str): The name of the person.
        email (str): The email address of the person.
        password (str): The password for the person's account.
        role (RoleEnum): The role of the person, which can be either 'Admin' or 'User'.
    """
    name: str
    email: str
    password: str
    role: RoleEnum

class User(Person):
    """
    Represents a user who inherits from the Person class.

    This class does not add any additional attributes or methods
    but serves as a specific type of Person with a 'User' role.
    """

class Admin(Person):
    """
    Represents an admin who inherits from the Person class.

    This class does not add any additional attributes or methods
    but serves as a specific type of Person with an 'Admin' role.
    """
