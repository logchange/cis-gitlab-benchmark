from src.common.logger import info
from src.controls.control import Control, ControlResult


class BranchDeletionDeniedControl(Control):

    def get_name(self):
        return "1.1.17 Ensure branch deletions are denied (Manual)"

    def validate(self, gl_group_project, gl_project) -> ControlResult:
        info(f"Project name: {gl_project.name} - Performing check {self.get_name()}")

        protected_branches = gl_project.protectedbranches.list(all=True)

        if len(protected_branches) == 0:
            return ControlResult(self.get_name(), False, f"Repository does not have protected branches!")

        return ControlResult(self.get_name(), True, "")
