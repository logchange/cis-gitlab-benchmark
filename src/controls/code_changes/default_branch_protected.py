from src.common.logger import info
from src.controls.control import Control, ControlResult


class DefaultBranchProtectedControl(Control):

    def get_name(self):
        return "1.1.20 Ensure branch protection is enforced on the default branch (Manual)"

    def validate(self, gl_group_project, gl_project) -> ControlResult:
        info(f"Project name: {gl_project.name} - Performing check {self.get_name()}")

        default_branch = gl_project.default_branch

        protected_branches = gl_project.protectedbranches.list(all=True)

        for branch in protected_branches:

            if branch.name == default_branch:
                return ControlResult(self.get_name(), True, "")

        return ControlResult(self.get_name(), False, f"Default branch {default_branch} is not protected")
