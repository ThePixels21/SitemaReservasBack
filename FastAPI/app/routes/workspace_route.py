"""
This module defines the API routes for managing workspaces and their schedules.

Routes:
    - GET /workspaces: Retrieve a list of all workspaces.
    - GET /workspaces/{workspace_id}: Retrieve a specific workspace by its ID.
    - POST /workspaces: Create a new workspace.
    - PUT /workspaces/{workspace_id}: Update an existing workspace.
    - DELETE /workspaces/{workspace_id}: Delete a workspace and its schedules.
    - POST /workspaces/{workspace_id}/schedules: Add a new schedule to a workspace.
    - DELETE /schedules/{schedule_id}: Delete a specific schedule by ID.
"""
from http.client import HTTPException
from typing import Optional, List

from database import PersonModel # pylint: disable=import-error
from helpers.api_key_auth import admin_required # pylint: disable=import-error
from models.workspace import Workspace # pylint: disable=import-error
from models.schedule import Schedule # pylint: disable=import-error
from services.workspace_service import WorkspaceService # pylint: disable=import-error
from services import schedule_service # pylint: disable=import-error

from fastapi import APIRouter, Body, Depends, Query

workspace_route = APIRouter()
workspace_service = WorkspaceService()
schedule_service = schedule_service.ScheduleService()

@workspace_route.get("/")
def get_workspaces():
    """
    Retrieve a list of all workspaces.

    Returns:
        list: A list of workspace objects.
    """
    return workspace_service.get_workspaces()

@workspace_route.get("/{workspace_id}")
def get_workspace(workspace_id: int):
    """
    Retrieve a specific workspace by its ID.

    Args:
        workspace_id (int): The ID of the workspace to retrieve.

    Returns:
        dict: A dictionary containing the workspace details and its schedules,
              or a message indicating the workspace was not found.
    """
    return workspace_service.get_workspace(workspace_id)

@workspace_route.post("/")
def create_workspace(
    workspace: Workspace = Body(...),
    _current_user: PersonModel = Depends(admin_required)
):
    """
    Create a new workspace.

    Args:
        workspace (Workspace): The workspace object to create.
        _current_user (PersonModel): The current user, must be an admin.

    Returns:
        dict: The created workspace object.
    """
    try:
        return workspace_service.create_workspace(workspace, created_by=_current_user.id)

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Error: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ha ocurrido un error inesperado: {str(e)}")


@workspace_route.put("/{workspace_id}")
def update_workspace(
    workspace_id: int,
    workspace: Workspace = Body(...),
    _current_user: PersonModel = Depends(admin_required)
):
    """
    Updates an existing workspace by its ID.

    ### Args
    - workspace_id (int): The unique identifier of the workspace.
    - workspace (Workspace): The workspace data to update.
    - _current_user (PersonModel): The current user, must be an admin.

    ### Returns
    - Workspace: The updated workspace information.
    """
    return workspace_service.update_workspace(workspace_id, workspace)


@workspace_route.delete("/{workspace_id}")
def delete_workspace(
        workspace_id: int,
        _current_user: PersonModel = Depends(admin_required)):
    """
    Delete a workspace and its schedules.

    Args:
        _current_user: PersonModel: The current user, must be an admin.
        workspace_id (int): The ID of the workspace to delete.

    Returns:
        str: A message indicating whether the deletion was successful.
    """
    return workspace_service.delete_workspace(workspace_id)

@workspace_route.post("/{workspace_id}/schedules")
def add_schedule(
        workspace_id: int, schedule: Schedule,
        _current_user: PersonModel = Depends(admin_required)):
    """
    Add a new schedule to a workspace.

    Args:
        workspace_id (int): The ID of the workspace to which the schedule will be added.
        schedule (Schedule): The schedule object containing the details of the schedule.
        _current_user (PersonModel): The current user, must be an admin.

    Returns:
        str: A message indicating whether the schedule was added successfully.

    Raises:
        HTTPException: If the workspace is not found.
    """
    result = schedule_service.add_schedule(workspace_id, {
        "opening_time": schedule.opening_time,
        "closing_time": schedule.closing_time,
        "status": schedule.status
    })
    if result == "Workspace not found":
        raise HTTPException(status_code=404, detail="Workspace not found")
    return result

@workspace_route.delete("/schedules/{schedule_id}")
def delete_schedule(
        schedule_id: int,
        _current_user: PersonModel = Depends(admin_required)
):
    """
    Delete a specific schedule by ID.

    Args:
        _current_user:
        schedule_id (int): The ID of the schedule to delete.

    Returns:
        str: A message indicating whether the deletion was successful.
    """
    return schedule_service.delete_schedule(schedule_id)

@workspace_route.get("/workspaces/filter", response_model=List[Workspace])
def filter_workspaces(
    workspace_type: Optional[str] = Query(None, description="Workspace type (e.g., office, meeting room)"),
    min_capacity: Optional[int] = Query(None, gt=0, description="Minimum capacity of the workspace"),
    date: Optional[str] = Query(None, description="Available date in format YYYY-MM-DD"),
    time: Optional[str] = Query(None, description="Available time in format HH:MM"),
):
    """
    Filter workspaces by type, minimum capacity, and availability by date/time.

    Args:
        workspace_type (Optional[str]): The type of workspace (e.g., office, meeting room).
        min_capacity (Optional[int]): The minimum capacity of the workspace.
        date (Optional[str]): The desired date in YYYY-MM-DD format.
        time (Optional[str]): The desired time in HH:MM format.

    Returns:
        List[Workspace]: List of workspaces that match the filters.
    """
    workspaces = workspace_service.filter_workspaces(workspace_type, min_capacity, date, time)
    if not workspaces:
        raise HTTPException(status_code=404, detail="No workspaces found with the specified filters")
    return workspaces
