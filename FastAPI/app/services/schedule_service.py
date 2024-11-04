from peewee import DoesNotExist

from database import WorkspaceModel, ScheduleModel


class ScheduleService:
    """
    Service class for managing schedules.
    """
    def add_schedule(self, workspace_id: int, schedule_data: dict):
        """
        Add a new schedule to a workspace.
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


    def delete_schedule(self, schedule_id: int):
        """
        Delete a specific schedule by ID.
        """
        try:
            schedule = ScheduleModel.get(ScheduleModel.id == schedule_id)
            schedule.delete_instance()
            return "Schedule deleted successfully"
        except DoesNotExist:
            return "Schedule not found"