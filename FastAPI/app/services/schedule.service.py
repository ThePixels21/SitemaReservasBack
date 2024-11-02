from peewee import DoesNotExist

from FastAPI.app.database import WorkspaceModel, ScheduleModel


def add_schedule(self, workspace_id: int, schedule_data: dict):
    """
    Add a new schedule to a workspace.
    """
    try:
        workspace = WorkspaceModel.get(WorkspaceModel.id == workspace_id)
        ScheduleModel.create(
            openingTime=schedule_data['openingTime'],
            closingTime=schedule_data['closingTime'],
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