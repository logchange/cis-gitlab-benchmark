from src.common.logger import info
from src.controls.control import Control, ControlResult


class RepositoryForksControl(Control):

    def __init__(self, config: dict):
        control_dict = config.get('gitlab').get('repository_management').get('repository_forks')
        enabled = control_dict.get('enabled')
        super().__init__(enabled)
        self.max_number_of_forks = control_dict.get("max_number_of_forks")

    def get_name(self):
        return "1.2.5 Ensure all copies (forks) of code are tracked and accounted for (Manual)"

    def validate_specific(self, gl_group_project, gl_project) -> ControlResult:
        forks_count = gl_project.forks_count

        if forks_count == 0:
            return ControlResult(self.get_name(), True, "")
        else:
            forks = gl_project.forks.list(all=True)
            forks_more_info = f"Number of forks: {forks_count} Forks location:\n"

            for fork in forks:
                forks_more_info += f"- {fork.name_with_namespace}"

            return ControlResult(self.get_name(), False, forks_more_info)
