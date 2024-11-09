"""
Main module for FastAPI application setup.

This module sets up the FastAPI application, manages the database connection
lifecycle, and includes routes.
"""
from contextlib import asynccontextmanager

from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from database import initialize_database, database as connection
from helpers.api_key_auth import get_api_key
from routes.user_route import user_route
from routes.workspace_route import workspace_route
from fastapi import FastAPI,Depends

@asynccontextmanager
async def manage_lifespan(_app: FastAPI):
    """
    Manage the lifespan of the FastAPI application.

    Ensures the database connection is opened and closed properly.
    """
    if connection.is_closed():
        connection.connect()
    try:
        initialize_database()
        yield
    finally:
        if not connection.is_closed():
            connection.close()

app = FastAPI(
    lifespan=manage_lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    """
    Redirect the root path to the API documentation.

    Returns a redirection response to the documentation page.
    """
    return RedirectResponse(url="/docs")

app.include_router(user_route,prefix="/users",tags=["Users"],dependencies=[Depends(get_api_key)])
app.include_router(
    workspace_route,
    prefix="/workspaces",
    tags=["workspaces"],
    dependencies=[Depends(get_api_key)]
)
