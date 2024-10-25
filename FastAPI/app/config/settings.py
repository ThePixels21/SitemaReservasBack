"""settings"""

from dotenv import load_dotenv
import os

ENV = os.getenv("RUN_ENV", "dev")

if ENV == "production":
    DATABASE = {
        "user": os.getenv("MYSQL_USER"),
        "password": os.getenv("MYSQL_PASSWORD"),
        "host": os.getenv("MYSQL_HOST"),
        "name": os.getenv("MYSQL_DATABASE"),
        "port": int(os.getenv("MYSQL_PORT")),
        "engine": "peewee.MySQLDatabase",
    }
else:
    DATABASE = {
        "user": os.getenv("MYSQL_USER"),
        "password": os.getenv("MYSQL_PASSWORD"),
        "host": os.getenv("MYSQL_HOST"),
        "name": os.getenv("MYSQL_DATABASE"),
        "port": int(os.getenv("MYSQL_PORT")),
        "engine": "peewee.MySQLDatabase",
    }  