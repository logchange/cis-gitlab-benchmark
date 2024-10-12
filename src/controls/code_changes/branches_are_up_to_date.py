from src.common.logger import info
from src.controls.control import Control, ControlResult


class BranchesAreUpToDateControl(Control):

    ALLOWED_MERGE_METHOD = ['rebase_merge', 'ff']

    def get_name(self):
        return "1.1.10 Ensure open Git branches are up to date before they can be merged into code base (Manual)"

    def validate(self, gl_group_project, gl_project) -> ControlResult:
        info(f"Project name: {gl_project.name} - Performing check {self.get_name()}")

        merge_method = gl_project.merge_method
        merge_method_passed = merge_method in self.ALLOWED_MERGE_METHOD

        merge_pipelines_enabled = gl_project.merge_pipelines_enabled
        merge_trains_enabled = gl_project.merge_trains_enabled

        if merge_method_passed and merge_pipelines_enabled and merge_trains_enabled:
            return ControlResult(self.get_name(), True, "")
        else:
            return ControlResult(self.get_name(), False,
                                 f"Merge method: {merge_method} allowed {self.ALLOWED_MERGE_METHOD}\nmerge pipelines enabled: {merge_pipelines_enabled}\nmerge trains enabled: {merge_trains_enabled}")
