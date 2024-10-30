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
from fastapi import APIRouter, Body

from FastAPI.app.models.workspace import Workspace
from FastAPI.app.services.workspace_service import WorkspaceService

router = APIRouter()
workspace_service = WorkspaceService()

@router.get("/workspaces")
def get_workspaces():
    """
    Retrieve a list of all workspaces.

    Returns:
        list: A list of workspace objects.
    """
    return workspace_service.get_workspaces()

@router.get("/workspaces/{workspace_id}")
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

@router.post("/workspaces")
def create_workspace(workspace: Workspace = Body(...)):
    """
    Create a new workspace.

    Args:
        workspace (Workspace): The workspace object to create.

    Returns:
        Workspace: The created workspace object.
    """
    return workspace_service.create_workspace(workspace)

@router.put("/workspaces/{workspace_id}")
def update_workspace(workspace_id: int, workspace_data: dict):
    """
    Update an existing workspace.

    Args:
        workspace_id (int): The ID of the workspace to update.
        workspace_data (dict): A dictionary containing the updated workspace data.

    Returns:
        str: A message indicating whether the update was successful.
    """
    return workspace_service.update_workspace(workspace_id, workspace_data)

def delete_workspace(workspace_id: int):
    """
    Delete a workspace and its schedules.

    Args:
        workspace_id (int): The ID of the workspace to delete.

    Returns:
        str: A message indicating whether the deletion was successful.
    """
    return workspace_service.delete_workspace(workspace_id)

@router.post("/workspaces/{workspace_id}/schedules")
def add_schedule(workspace_id: int, schedule_data: dict):
    """
    Add a new schedule to a workspace.

    Args:
        workspace_id (int): The ID of the workspace to add the schedule to.
        schedule_data (dict): A dictionary containing the schedule details.

    Returns:
        str: A message indicating whether the schedule was added successfully.
    """
    return workspace_service.add_schedule(workspace_id, schedule_data)

def delete_schedule(schedule_id: int):
    """
    Delete a specific schedule by ID.

    Args:
        schedule_id (int): The ID of the schedule to delete.

    Returns:
        str: A message indicating whether the deletion was successful.
    """
    return workspace_service.delete_schedule(schedule_id)
