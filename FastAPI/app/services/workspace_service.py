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
from typing import Optional, List

from peewee import DoesNotExist, IntegrityError

from database import (WorkspaceModel, ScheduleModel)
from models.workspace import Workspace

from fastapi import Body, HTTPException


# pylint: enable=unused-import

class WorkspaceService:
    """
     Service class for managing workspaces and their schedules.
    """
    def get_workspaces(self):
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

    def get_workspace(self, workspace_id: int):
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
    def create_workspace(workspace: Workspace, created_by: int):
        """
        Create a new workspace.

        Args:
            workspace (Workspace): The workspace data to create.
            created_by (int): The ID of the user creating the workspace.

        Returns:
            Workspace: The created workspace object.
        """
        new_workspace = WorkspaceModel.create(
            type=workspace.type.value,
            capacity=workspace.capacity,
            hourlyRate=workspace.hourlyRate,
            created_by=created_by
        )
        return new_workspace

    @staticmethod
    def update_workspace(workspace_id: int, workspace: Workspace):
        """
        Updates an existing workspace's information in the database.

        ### Args:
        - workspace_id (int): The ID of the workspace to update.
        - workspace (Workspace): A Pydantic model instance representing the updated workspace data.

        ### Returns:
        - WorkspaceModel: The updated workspace.

        ### Raises:
        - HTTPException: If the workspace is not found or the update fails.
        """
        try:
            # Find the workspace to update
            existing_workspace = WorkspaceModel.get(WorkspaceModel.id == workspace_id)

            # Validate and update fields
            existing_workspace.type = workspace.type.value or existing_workspace.type
            existing_workspace.capacity = workspace.capacity or existing_workspace.capacity
            existing_workspace.hourlyRate = workspace.hourlyRate or existing_workspace.hourlyRate

            # Save changes to the database
            existing_workspace.save()
            return existing_workspace

        except DoesNotExist as exc:
            raise HTTPException(status_code=404, detail="Workspace not found") from exc
        except IntegrityError as exc:
            raise HTTPException(status_code=400, detail="Could not update workspace") from exc

    @staticmethod
    def delete_workspace( workspace_id: int):
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

    def filter_workspaces(
            self,
            workspace_type: Optional[str],
            min_capacity: Optional[int],
            date: Optional[str],
            time: Optional[str],
    ) -> List[WorkspaceModel]:
        query = WorkspaceModel.select()

        if workspace_type:
            query = query.where(WorkspaceModel.type == workspace_type)
        if min_capacity:
            query = query.where(WorkspaceModel.capacity >= min_capacity)
        if date and time:
            datetime_requested = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            query = query.join(ScheduleModel).where(
                (ScheduleModel.opening_time <= datetime_requested) &
                (ScheduleModel.closing_time >= datetime_requested) &
                (ScheduleModel.status == "Available")
            )

        return list(query)
