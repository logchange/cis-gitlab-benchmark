from datetime import timedelta, timezone, datetime

from dateutil.parser import isoparse

from src.controls.control import Control, ControlResult


class RepositoryInactivityControl(Control):
    def __init__(self, config: dict):
        control_dict = config.get('gitlab').get('repository_management').get('inactive_repositories')
        enabled = control_dict.get('enabled')
        super().__init__(enabled)
        self.max_number_of_inactive_days = control_dict.get("max_number_of_inactive_days")

    def get_name(self):
        return "1.2.7 Ensure inactive repositories are reviewed and archived periodically (Manual)"

    def validate_specific(self, gl_group_project, gl_project) -> ControlResult:
        last_activity = isoparse(gl_project.last_activity_at)

        last_activity_threshold = datetime.now(timezone.utc) - timedelta(days=self.max_number_of_inactive_days)

        if last_activity < last_activity_threshold:
            return ControlResult(self.get_name(), False,
                                 f"Project with no activity for more than {self.max_number_of_inactive_days}, last activity at: {last_activity}")
        else:
            return ControlResult(self.get_name(), True, f"Last activity at: {last_activity}")



