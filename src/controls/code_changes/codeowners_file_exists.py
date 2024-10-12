from src.common.gitlab_client import file_exists
from src.common.logger import info
from src.controls.control import Control, ControlResult


class CodeOwnersFileExistsControl(Control):

    def get_name(self):
        return "1.1.6 Ensure code owners are set for extra sensitive code or configuration (Manual)"

    def validate(self, gl_group_project, gl_project) -> ControlResult:
        info(f"Project name: {gl_project.name} - Performing check {self.get_name()}")
        if file_exists(gl_project, 'CODEOWNERS'):
            return ControlResult(self.get_name(), True, "")
        else:
            return ControlResult(self.get_name(), False, "CODEOWNERS file does not exists")
