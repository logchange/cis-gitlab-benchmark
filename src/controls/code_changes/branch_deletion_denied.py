from src.controls.control import Control, ControlResult


class BranchDeletionDeniedControl(Control):

    def __init__(self, config: dict):
        control_dict = config.get('gitlab').get('code_changes').get('branch_deletion_denied')
        enabled = control_dict.get('enabled')
        super().__init__(enabled)

    def get_name(self):
        return "1.1.17 Ensure branch deletions are denied (Manual)"

    def validate_specific(self, gl_group_project, gl_project) -> ControlResult | None:
        protected_branches = gl_project.protectedbranches.list(all=True)

        if len(protected_branches) == 0:
            return ControlResult(self.get_name(), False, f"Repository does not have protected branches!")

        return ControlResult(self.get_name(), True, "")
