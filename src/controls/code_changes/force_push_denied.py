from src.common.logger import info
from src.controls.control import Control, ControlResult


class ForcePushDeniedControl(Control):

    def get_name(self):
        return "1.1.16 Ensure force push code to branches is denied (Manual)"

    def validate(self, gl_group_project, gl_project) -> ControlResult:
        info(f"Project name: {gl_project.name} - Performing check {self.get_name()}")

        protected_branches = gl_project.protectedbranches.list(all=True)

        if len(protected_branches) == 0:
            return ControlResult(self.get_name(), False,
                                 f"Repository does not have protected branches!")

        passed = True
        more_info = ""

        for branch in protected_branches:

            allow_force_push = branch.allow_force_push

            if allow_force_push:
                passed = False
                more_info += f"For branch: {branch.name} force pushed allowed\n"

        return ControlResult(self.get_name(), passed, more_info)
