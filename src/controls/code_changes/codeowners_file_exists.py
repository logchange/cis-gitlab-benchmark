from src.common.gitlab_client import file_exists
from src.controls.control import Control, ControlResult


class CodeOwnersFileExistsControl(Control):
    
    def __init__(self, config: dict):
        control_dict = config.get('gitlab').get('code_changes').get('codeowners_file_exists')
        enabled = control_dict.get('enabled')
        super().__init__(enabled)

    def get_name(self):
        return "1.1.6 Ensure code owners are set for extra sensitive code or configuration (Manual)"

    def validate_specific(self, gl_group_project, gl_project) -> ControlResult:
        if file_exists(gl_project, 'CODEOWNERS'):
            return ControlResult(self.get_name(), True, "")
        else:
            return ControlResult(self.get_name(), False, "CODEOWNERS file does not exists")
