from src.common.gitlab_client import file_exists
from src.common.logger import info
from src.controls.control import Control, ControlResult


class SecurityFileExistsControl(Control):

    def get_name(self):
        return "1.2.1 Ensure all public repositories contain a SECURITY.md file (Manual)"

    def validate(self, gl_group_project, gl_project) -> ControlResult:
        info(f"Project name: {gl_project.name} - Performing check {self.get_name()}")
        if file_exists(gl_project, 'SECURITY.md'):
            return ControlResult(self.get_name(), True, "")
        else:
            return ControlResult(self.get_name(), False, "SECURITY.md file does not exists")
