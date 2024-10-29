from datetime import datetime, timedelta, timezone

from dateutil.parser import isoparse

from src.common.logger import info
from src.controls.control import Control, ControlResult


class StaleBranchesRemovedControl(Control):

    def __init__(self, config: dict):
        control_dict = config.get('gitlab').get('code_changes').get('stale_branches')
        enabled = control_dict.get('enabled')
        super().__init__(enabled)
        self.stale_days = control_dict.get("stale_days")

    def get_name(self):
        return "1.1.8 Ensure inactive branches are periodically reviewed and removed (Manual)"

    def validate_specific(self, gl_group_project, gl_project) -> ControlResult:
        branches = gl_project.branches.list(all=True)

        merged_count = 0
        stale_count = 0
        stale_threshold = datetime.now(timezone.utc) - timedelta(days=self.stale_days)

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
