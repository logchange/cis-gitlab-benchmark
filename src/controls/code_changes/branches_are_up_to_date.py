from src.controls.control import Control, ControlResult


class BranchesAreUpToDateControl(Control):

    def __init__(self, config: dict):
        control_dict = config.get('gitlab').get('code_changes').get('branches_are_up_to_date')
        enabled = control_dict.get('enabled')
        super().__init__(enabled)
        self.allowed_merge_method = control_dict.get('allowed_merge_method')

    def get_name(self):
        return "1.1.10 Ensure open Git branches are up to date before they can be merged into code base (Manual)"

    def validate_specific(self, gl_group_project, gl_project) -> ControlResult | None:
        merge_method = gl_project.merge_method
        merge_method_passed = merge_method in self.allowed_merge_method

        merge_pipelines_enabled = gl_project.merge_pipelines_enabled
        merge_trains_enabled = gl_project.merge_trains_enabled

        if merge_method_passed and merge_pipelines_enabled and merge_trains_enabled:
            return ControlResult(self.get_name(), True, "")
        else:
            return ControlResult(self.get_name(), False,
                                 f"Merge method: {merge_method} allowed {self.allowed_merge_method}\nmerge pipelines enabled: {merge_pipelines_enabled}\nmerge trains enabled: {merge_trains_enabled}")
