from src.common.logger import info
from src.controls.control import Control, ControlResult


class DefaultBranchProtectedControl(Control):

    def __init__(self, config: dict):
        control_dict = config.get('gitlab').get('code_changes').get('default_branch_protected')
        enabled = control_dict.get('enabled')
        super().__init__(enabled)

    def get_name(self):
        return "1.1.20 Ensure branch protection is enforced on the default branch (Manual)"

    def validate_specific(self, gl_group_project, gl_project) -> ControlResult:
        default_branch = gl_project.default_branch

        protected_branches = gl_project.protectedbranches.list(all=True)

        for branch in protected_branches:

            if branch.name == default_branch:
                return ControlResult(self.get_name(), True, "")

        return ControlResult(self.get_name(), False, f"Default branch {default_branch} is not protected")
