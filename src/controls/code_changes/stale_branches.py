from datetime import datetime, timedelta, timezone

from dateutil.parser import isoparse

from src.common.logger import info
from src.controls.control import Control, ControlResult


class StaleBranchesRemovedControl(Control):
    STALE_DAYS = 90

    def get_name(self):
        return "1.1.8 Ensure inactive branches are periodically reviewed and removed (Manual)"

    def validate(self, gl_group_project, gl_project) -> ControlResult:
        info(f"Project name: {gl_project.name} - Performing check {self.get_name()}")
        branches = gl_project.branches.list(all=True)

        merged_count = 0
        stale_count = 0
        stale_threshold = datetime.now(timezone.utc) - timedelta(days=self.STALE_DAYS)

        for branch in branches:
            if branch.merged:
                merged_count += 1
            else:
                last_commit_date = isoparse(branch.commit['committed_date'])
                if last_commit_date < stale_threshold:
                    stale_count += 1

        if stale_count == 0 and merged_count == 0:
            return ControlResult(self.get_name(), True, "")
        else:
            return ControlResult(self.get_name(), False,
                                 f"Stale branches count: {stale_count}, merged but not deleted branches count: {merged_count}")
