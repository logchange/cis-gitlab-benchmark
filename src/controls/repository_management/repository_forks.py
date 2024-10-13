from src.common.logger import info
from src.controls.control import Control, ControlResult


class RepositoryForksControl(Control):
    MAX_NUMBER_OF_FORKS = 0

    def get_name(self):
        return "1.2.5 Ensure all copies (forks) of code are tracked and accounted for (Manual)"

    def validate(self, gl_group_project, gl_project) -> ControlResult:
        info(f"Project name: {gl_project.name} - Performing check {self.get_name()}")

        forks_count = gl_project.forks_count

        if forks_count == 0:
            return ControlResult(self.get_name(), True, "")
        else:
            forks = gl_project.forks.list(all=True)
            forks_more_info = f"Number of forks: {forks_count} Forks location:\n"

            for fork in forks:
                forks_more_info += f"- {fork.name_with_namespace}"

            return ControlResult(self.get_name(), False, forks_more_info)
