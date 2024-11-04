"""
Schedule Service Module

This module provides services for managing schedules within the application.
It includes functionalities to add and delete schedules associated with workspaces.

Classes:
    ScheduleService: Service class for managing schedules.

Methods:
    add_schedule(workspace_id: int, schedule_data: dict) -> str:
        Adds a new schedule to a workspace.

    delete_schedule(schedule_id: int) -> str:
        Deletes a specific schedule by ID.
"""
from peewee import DoesNotExist
from database import WorkspaceModel, ScheduleModel

class ScheduleService:
    """
    Service class for managing schedules.
    """

    def add_schedule(self, workspace_id: int, schedule_data: dict) -> str:
        """
        Add a new schedule to a workspace.

        Args:
            workspace_id (int): The ID of the workspace to which the schedule will be added.
            schedule_data (dict): A dictionary containing the schedule details.

        Returns:
            str: A message indicating the result of the operation.
        """
        try:
            workspace = WorkspaceModel.get(WorkspaceModel.id == workspace_id)
            ScheduleModel.create(
                opening_time=schedule_data['opening_time'],
                closing_time=schedule_data['closing_time'],
                status=schedule_data['status'],
                workspace=workspace
            )
            return "Schedule added successfully"
        except DoesNotExist:
            return "Workspace not found"

    def delete_schedule(self, schedule_id: int) -> str:
        """
        Delete a specific schedule by ID.

        Args:
            schedule_id (int): The ID of the schedule to be deleted.

        Returns:
            str: A message indicating the result of the operation.
        """
        try:
            schedule = ScheduleModel.get(ScheduleModel.id == schedule_id)
            schedule.delete_instance()
            return "Schedule deleted successfully"
        except DoesNotExist:
            return "Schedule not found"