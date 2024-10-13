from datetime import timedelta, timezone, datetime

from dateutil.parser import isoparse

from src.common.logger import info
from src.controls.control import Control, ControlResult


class RepositoryInactivityControl(Control):
    MAX_NUMBER_OF_INACTIVE_DAYS = 180

    def get_name(self):
        return "1.2.7 Ensure inactive repositories are reviewed and archived periodically (Manual)"

    def validate(self, gl_group_project, gl_project) -> ControlResult:
        info(f"Project name: {gl_project.name} - Performing check {self.get_name()}")

        last_activity = isoparse(gl_project.last_activity_at)

        last_activity_threshold = datetime.now(timezone.utc) - timedelta(days=self.MAX_NUMBER_OF_INACTIVE_DAYS)

        if last_activity < last_activity_threshold:
            return ControlResult(self.get_name(), False, f"Project with no activity for more than {self.MAX_NUMBER_OF_INACTIVE_DAYS}, last activity at: {last_activity}")
        else:
            return ControlResult(self.get_name(), True, f"Last activity at: {last_activity}")



