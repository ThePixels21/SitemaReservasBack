"""
This module defines the models for managing users, roles, and groups in the system,
using the Peewee ORM for MySQL database interactions. It establishes relationships 
between users, roles, and groups and includes cascading delete behaviors.
"""

from peewee import Model, MySQLDatabase, AutoField, CharField  # type: ignore
from config.settings import DATABASE  # pylint: disable=E0401

print(DATABASE)

# Configure the MySQL database connection
database = MySQLDatabase(
    DATABASE["name"],
    user=DATABASE["user"],
    password=DATABASE["password"],
    host=DATABASE["host"],
    port=int(DATABASE["port"]),
)


class PersonModel(Model):
    """
    Represents a person with attributes such as ID,
    name, email, password, and role.
    """

    id = AutoField()
    name = CharField()
    email = CharField()
    password = CharField()
    role = CharField()
    # pylint: disable=too-few-public-methods
    class Meta:

        """
        Meta class for PersonModel.
        """
        database = database
        table_name = "person"


class PromotionModel(Model):
    """
    Represents a promotion with attributes such as ID, description, discount, start time,
    end time, status, reservation, and created by.
    """

    id = AutoField()
    description = CharField()
    discount = CharField()
    startTime = CharField()
    endTime = CharField()
    status = CharField()
    reservation = CharField()
    createdBy = CharField()
    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta class for PromotionModel.  
        """
        database = database
        table_name = "promotion"


class ReservationModel(Model):
    """
    Represents a reservation with attributes such as ID,
    reserved by, workspace, start time, end time, status, and price.
    """

    id = AutoField()
    reservedBy = CharField()
    workspace = CharField()
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


class ScheduleModel(Model):
    """
    Represents a schedule with attributes such as ID,
    opening time, closing time, and status.
    """

    id = AutoField()
    openingTime = CharField()
    closingTime = CharField()
    status = CharField()
    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta class for ScheduleModel.
        """
        database = database
        table_name = "schedule"


class WorkspaceModel(Model):
    """
    represents a workspace with attributes such as ID, type,
      capacity, hourly rate, available schedules, and created by.
    """

    id = AutoField()
    type = CharField()
    capacity = CharField()
    hourlyRate = CharField()
    availableSchedules = CharField()
    createdBy = CharField()
    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta class for WorkspaceModel.
        """
        database = database
        table_name = "workspace"
