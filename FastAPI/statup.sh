#!/bin/sh

# Start Migrations
alembic merge heads
alembic stamp head
alembic revision --autogenerate -m 'autorevision migratios'
alembic upgrade head

# Start the backend...
uvicorn main:app --host 0.0.0.0 --reload --port 80