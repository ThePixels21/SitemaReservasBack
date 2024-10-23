"""
This module defines the models for managing users, roles, and groups in the system,
using the Peewee ORM for MySQL database interactions. It establishes relationships 
between users, roles, and groups and includes cascading delete behaviors.
"""

import os
from dotenv import load_dotenv
from peewee import Model, MySQLDatabase, DateField, AutoField, CharField

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
