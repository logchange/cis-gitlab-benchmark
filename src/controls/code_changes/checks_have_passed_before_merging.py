from src.common.logger import info
from src.controls.control import Control, ControlResult


class AllChecksHavePassedBeforeMergingControl(Control):

    def get_name(self):
        return "1.1.9 Ensure all checks have passed before merging new code (Manual)"

    def validate(self, gl_group_project, gl_project) -> ControlResult:
        info(f"Project name: {gl_project.name} - Performing check {self.get_name()}")

        pipeline_succeeds = gl_project.only_allow_merge_if_pipeline_succeeds

        try:
            status_checks_passed = gl_project.only_allow_merge_if_all_status_checks_passed
        except AttributeError:
            # only_allow_merge_if_all_status_checks_passed only available in Ultimate plan
            status_checks_passed = True

        if pipeline_succeeds and status_checks_passed:
            return ControlResult(self.get_name(), True, "")
        else:
            return ControlResult(self.get_name(), False,
                                 f"Pipeline must succeeds: {pipeline_succeeds},  Status checks must succeed(Ultimate) {status_checks_passed}")
