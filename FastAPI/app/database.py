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
        database.create_tables([PersonModel, WorkspaceModel, ScheduleModel], safe=True)
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
    created_by = CharField
    # created_by = ForeignKeyField(PersonModel, backref='workspaces')


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
