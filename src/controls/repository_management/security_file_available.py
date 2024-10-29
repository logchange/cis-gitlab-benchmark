from src.common.gitlab_client import file_exists
from src.controls.control import Control, ControlResult


class SecurityFileExistsControl(Control):
    
    def __init__(self, config: dict):
        control_dict = config.get('gitlab').get('repository_management').get('security_file_available')
        enabled = control_dict.get('enabled')
        super().__init__(enabled)

    def get_name(self):
        return "1.2.1 Ensure all public repositories contain a SECURITY.md file (Manual)"

    def validate_specific(self, gl_group_project, gl_project) -> ControlResult:
        if file_exists(gl_project, 'SECURITY.md'):
            return ControlResult(self.get_name(), True, "")
        else:
            return ControlResult(self.get_name(), False, "SECURITY.md file does not exists")
