"""
This module defines the models for managing users, roles, and groups in the system,
using the Peewee ORM for MySQL database interactions. It establishes relationships 
between users, roles, and groups and includes cascading delete behaviors.
"""

import os
from dotenv import load_dotenv
from peewee import (
    Model,
    MySQLDatabase,
    AutoField,
    CharField,
    IntegerField,
    DoubleField,
    DateTimeField,
    ForeignKeyField)

# Load environment variables from .env file
load_dotenv()

# Initialize the MySQL database connection using environment variables
database = MySQLDatabase(
    os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    passwd=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=int(os.getenv("MYSQL_PORT")),
)



# Secret key and token expiration settings
secret_key: str = os.getenv('SECRET_KEY')
token_expire: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))  # Default is now a string
access_token_expire_minutes = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

def initialize_database():
    """
    Initialize the database by creating the necessary tables.

    This function connects to the database and creates the tables for the
    `PersonModel`, `WorkspaceModel`, and `ScheduleModel` if they do not
    already exist.

    Returns:
        None
    """
    with database:
        database.create_tables([PersonModel, WorkspaceModel, ScheduleModel, ReservationModel,PromotionModel, permissionModel, RolePermissionModel], safe=True)
class PersonModel(Model):
    """
    Represents a person with attributes such as ID, name, email, password, and role.

    Attributes:
    - id (AutoField): Primary key for the person.
    - name (CharField): Name of the person (max length: 50).
    - email (CharField): Email address of the person (max length: 100).
    - password (CharField): Password for authentication (max length: 100).
    - role (CharField): Role assigned to the person (max length: 50).

    Meta:
    - database: Database connection.
    - table_name: Name of the table in the database.
    """
    id = AutoField(primary_key=True)
    name = CharField(max_length=50)
    email = CharField(max_length=100)
    password = CharField(max_length=100)
    role = CharField(max_length=50)

    class Meta:
        """
        Metadata for the PersonModel.

        Attributes:
        - database: Database connection.
        - table_name: Name of the table in the database.
        """
        # pylint: disable=too-few-public-methods
        database = database
        table_name = "person"

class permissionModel(Model):
    """
    Represents a permission with attributes such as ID and name.

    attributes: 
    - id: The unique identifier for the permission.
    - name: The name of the permission.
    """

    id = AutoField(primary_key=True)
    name = CharField()
    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Metadata for the PersonModel.

        Attributes:
        - database: Database connection.
        - table_name: Name of the table in the database.
        """
        database = database
        table_name = "permission"

class RolePermissionModel(Model):
    """
    Represents a role permission with attributes such as ID,
    permission, and person.

    atributes: 
    - id: The unique identifier for the role permission.
    - permission_id: The ID of the permission associated with the role permission.
    - person_id: The ID of the person associated with the role permission.
    """

    id = AutoField(primary_key=True)
    permission_id = ForeignKeyField(permissionModel, backref="role_permission")
    person_id = ForeignKeyField(PersonModel, backref="role_permission")
    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta class for RolePermissionModel.
        """
        database = database
        table_name = "role_permission"


class WorkspaceModel(Model):
    """
    Represents a workspace with attributes such as ID, type, capacity, hourly rate, and creator.

    Attributes:
    - id (AutoField): Primary key for the workspace.
    - type (CharField): Type of the workspace (max length: 50).
    - capacity (IntegerField): Capacity of the workspace.
    - hourlyRate (DoubleField): Hourly rate for using the workspace.
    - created_by (CharField): Creator of the workspace.
    """
    id = AutoField(primary_key=True)
    type = CharField(max_length=50)
    capacity = IntegerField()
    hourlyRate = DoubleField()
    created_by = ForeignKeyField(PersonModel, backref="workspace", column_name = "created_by")


    class Meta:
        """
        Metadata for the WorkspaceModel.

        Attributes:
        - database: Database connection.
        - table_name: Name of the table in the database.
        """
        # pylint: disable=too-few-public-methods
        database = database
        table_name = 'workspace'



class ReservationModel(Model):
    """
    Represents a reservation with attributes such as ID,
    reserved by, workspace, start time, end time, status, and price.

    atributes: 
    - id: The unique identifier for the reservation.
    - reservedBy: The user who made the reservation.
    - workspace: The workspace that is reserved.
    - startTime: The start time of the reservation.
    """

    id = AutoField(primary_key=True)
    reservedBy = ForeignKeyField(PersonModel, backref="reservation",column_name="reservedBy")
    workspace = ForeignKeyField(WorkspaceModel, backref="reservation",column_name="workspace")
    startTime = CharField()
    endTime = CharField()
    status = CharField()
    price = CharField()
    # pylint: disable=too-few-public-methods
    class Meta:

        """
        Meta class for ReservationModel.
        """
        database = database
        table_name = "reservation"



class PromotionModel(Model):
    """
    Represents a promotion with attributes such as ID, description, discount, start time,
    end time, status, reservation, and created by.

    atributes: 
    - id: The unique identifier for the promotion.
    - description: A brief description of the promotion.
    - discount: The discount percentage offered by the promotion.
    - startTime: The start time of the promotion.
    - endTime: The end time of the promotion.
    - status: The current status of the promotion.
    - reservation: The reservation associated with the promotion, if any.
    - createdBy: The user who created the promotion.
    """

    id = AutoField(primary_key=True)
    description = CharField()
    discount = CharField()
    startTime = CharField()
    endTime = CharField()
    status = CharField()
    reservation = ForeignKeyField(ReservationModel, backref="promotion")
    created_By = ForeignKeyField(PersonModel, backref="promotion")
    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta class for PromotionModel.  
        """
        database = database
        table_name = "promotion"



class ScheduleModel(Model):
    """
    Represents a schedule with attributes such as ID, opening time, closing time,
    status, and associated workspace.

    Attributes:
    - id (AutoField): Primary key for the schedule.
    - opening_time (DateTimeField): Opening time of the schedule.
    - closing_time (DateTimeField): Closing time of the schedule.
    - status (CharField): Status of the schedule.
    - workspace (ForeignKeyField): Associated workspace with a cascading delete behavior.
    """
    id = AutoField(primary_key=True)
    opening_time = DateTimeField()
    closing_time = DateTimeField()
    status = CharField()
    workspace = ForeignKeyField(WorkspaceModel, backref='schedules', on_delete='CASCADE')

    class Meta:
        """
        Metadata for the ScheduleModel.

        Attributes:
        - database: Database connection.
        - table_name: Name of the table in the database.
        """
        # pylint: disable=too-few-public-methods
        database = database
        table_name = 'schedule'
