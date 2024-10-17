from datetime import datetime
from enum import Enum

from pydantic.v1 import BaseModel

class RoleEnum(str, Enum):
    ADMIN = "Admin"
    USER = "User"

class Person(BaseModel):
    id: int
    name: str
    email: str
    password: str
    role: RoleEnum

class User(Person):
    pass

class Admin(Person):
    pass