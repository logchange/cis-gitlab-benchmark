from src.controls.control import Control, ControlResult


class LinearHistoryControl(Control):

    def __init__(self, config: dict):
        control_dict = config.get('gitlab').get('code_changes').get('linear_history')
        enabled = control_dict.get('enabled')
        super().__init__(enabled)
        self.allowed_merge_method = control_dict.get("allowed_merge_method")
        self.allowed_squash_options = control_dict.get("allowed_squash_options")

    def get_name(self):
        return "1.1.13 Ensure linear history is required (Manual)"

    def validate_specific(self, gl_group_project, gl_project) -> ControlResult:
        merge_method = gl_project.merge_method
        merge_method_passed = merge_method in self.allowed_merge_method  # only fast-forward

        squash_option = gl_project.squash_option
        squash_option_passed = squash_option in self.allowed_squash_options

        if merge_method_passed and squash_option_passed:
            return ControlResult(self.get_name(), True, "")
        else:
            return ControlResult(self.get_name(), False,
                                 f"Merge method: {merge_method} allowed {self.allowed_merge_method}\n" +
                                 f"Squash options: {squash_option}\nallowed: {self.allowed_squash_options}")
