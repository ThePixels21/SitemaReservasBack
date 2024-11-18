"""
Main module for FastAPI application setup.

This module sets up the FastAPI application, manages the database connection
lifecycle, and includes routes.
"""
from contextlib import asynccontextmanager

from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse, JSONResponse

from database import initialize_database, database as connection
from helpers.api_key_auth import get_api_key
from routes.user_route import user_route
from routes.workspace_route import workspace_route
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI,Depends, Request

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


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError): # pylint: disable=unused-argument
    """
    Handle validation errors for requests.

    Args:
        request (Request): The incoming request object.
        exc (RequestValidationError): The exception raised due to validation errors.

    Returns:
        JSONResponse: A JSON response with status code 422 and error details.
    """
    return JSONResponse(
        status_code=422,
        content={
            "detail": [{
                "msg": "Formato de entrada inválido. Por favor, verifique los campos y asegúrese"
                       " de que tienen los tipos correctos",
                "error_details": exc.errors()
            }]
        },
    )

app.include_router(user_route,prefix="/users",tags=["Users"],dependencies=[Depends(get_api_key)])
app.include_router(
    workspace_route,
    prefix="/workspaces",
    tags=["workspaces"],
    dependencies=[Depends(get_api_key)]
)
