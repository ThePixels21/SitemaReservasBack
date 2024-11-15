"""
This module provides services for managing workspaces and their schedules.

Classes:
    - WorkspaceService: A service class for managing workspaces and their schedules.

Methods:
    - get_workspaces: Retrieves all workspaces, including their schedules.
    - get_workspace: Retrieves a specific workspace along with its schedules.
    - create_workspace: Creates a new workspace.
    - update_workspace: Updates an existing workspace.
    - delete_workspace: Deletes a workspace and its schedules if no future schedules are assigned.
"""
from datetime import datetime

from peewee import DoesNotExist

from database import (WorkspaceModel, ScheduleModel)
from models.workspace import Workspace

from fastapi import Body

class WorkspaceService:
    """
     Service class for managing workspaces and their schedules.
    """
    @staticmethod
    def get_workspaces():
        """
        Get all workspaces, including their schedules.
        """
        workspaces = WorkspaceModel.select().dicts()
        results = []

        for workspace in workspaces:
            schedules = ScheduleModel.select().where(
                ScheduleModel.workspace == workspace['id']
            ).dicts()
            workspace['schedules'] = list(schedules)
            results.append(workspace)

        return results

    @staticmethod
    def get_workspace(workspace_id: int):
        """
        Get a specific workspace along with its schedules.
        """
        try:
            workspace = WorkspaceModel.get(WorkspaceModel.id == workspace_id)
            schedules = ScheduleModel.select().where(ScheduleModel.workspace==workspace_id).dicts()
            return {**workspace.__data__, 'schedules': list(schedules)}
        except DoesNotExist:
            return "Workspace not found"

    @staticmethod
    def create_workspace(workspace: Workspace = Body(...)):
        """
        Create a new workspace.
        """
        WorkspaceModel.create(
            type=workspace.type.value,
            capacity=workspace.capacity,
            hourlyRate=workspace.hourlyRate,
            created_by=workspace.createdBy
        )
        return workspace

    @staticmethod
    def update_workspace(workspace_id: int, workspace_data: dict):
        """
        Update an existing workspace.
        """
        WorkspaceModel.update(workspace_data).where(WorkspaceModel.id == workspace_id).execute()
        return "Workspace updated successfully"

    @staticmethod
    def delete_workspace(workspace_id: int):
        """
        Delete a workspace and its schedules if no future schedules are assigned.

        Args:
            workspace_id (int): The ID of the workspace to delete.

        Returns:
            str: A message indicating the result of the deletion attempt.
        """
        try:
            # Check for future schedules
            future_schedules = ScheduleModel.select().where(
                (ScheduleModel.id == workspace_id) &
                (ScheduleModel.opening_time > datetime.now())
            )

            if future_schedules.exists():
                return "Cannot delete workspace with future schedules assigned."

            # Delete the workspace if no future schedules
            workspace = WorkspaceModel.get(WorkspaceModel.id == workspace_id)
            workspace.delete_instance()
            return "Workspace deleted successfully"

        except DoesNotExist:
            return "Workspace not found"
