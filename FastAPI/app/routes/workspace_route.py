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

from fastapi import APIRouter, Body, Depends

from database import PersonModel
from helpers.api_key_auth import admin_required
from models.workspace import Workspace
from models.schedule import Schedule
from services.workspace_service import WorkspaceService
from services import schedule_service


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
    return workspace_service.create_workspace(workspace)

@workspace_route.put("/{workspace_id}")
def update_workspace(
        workspace_id: int,
        workspace_data: dict,
        _current_user: PersonModel = Depends(admin_required)):
    """
    Update an existing workspace.

    Args:
        _current_user: The current user, must be an admin.
        workspace_id (int): The ID of the workspace to update.
        workspace_data (dict): A dictionary containing the updated workspace data.

    Returns:
        str: A message indicating whether the update was successful.
    """
    return workspace_service.update_workspace(workspace_id, workspace_data)

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
    return workspace_service.delete_schedule(schedule_id)
