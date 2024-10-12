from src.common.logger import info
from src.controls.control import Control, ControlResult


class LinearHistoryControl(Control):
    ALLOWED_MERGE_METHOD = ['ff']
    ALLOWED_SQUASH_OPTIONS = ['default_on', 'always']

    def get_name(self):
        return "1.1.13 Ensure linear history is required (Manual)"

    def validate(self, gl_group_project, gl_project) -> ControlResult:
        info(f"Project name: {gl_project.name} - Performing check {self.get_name()}")

        merge_method = gl_project.merge_method
        merge_method_passed = merge_method in self.ALLOWED_MERGE_METHOD  # only fast-forward

        squash_option = gl_project.squash_option
        squash_option_passed = squash_option in self.ALLOWED_SQUASH_OPTIONS

        if merge_method_passed and squash_option_passed:
            return ControlResult(self.get_name(), True, "")
        else:
            return ControlResult(self.get_name(), False,
                                 f"Merge method: {merge_method} allowed {self.ALLOWED_MERGE_METHOD}\n" +
                                 f"Squash options: {squash_option}\nallowed: {self.ALLOWED_SQUASH_OPTIONS}")
