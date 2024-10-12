from src.controls.control import Control, ControlResult


class ApprovalDismissedControl(Control):

    def get_name(self):
        return "1.1.4 Ensure previous approvals are dismissed when updates are introduced to a code change proposal (Manual)"

    def validate(self, gl_group_project, gl_project) -> ControlResult:
        approvals = gl_project.approvals.get()

        if approvals.reset_approvals_on_push:
            return ControlResult(self.get_name(), True, "")
        else:
            return ControlResult(self.get_name(), False, "")
