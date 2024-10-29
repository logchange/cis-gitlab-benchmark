from src.common.logger import info
from src.controls.control import Control, ControlResult


class PushingOrMergingRestrictionControl(Control):
    
    def __init__(self, config: dict):
        control_dict = config.get('gitlab').get('code_changes').get('pushing_or_merging_restriction')
        enabled = control_dict.get('enabled')
        super().__init__(enabled)
        self.allowed_merge_access_levels = control_dict.get("allowed_merge_access_levels")
        self.allowed_push_access_levels = control_dict.get("allowed_push_access_levels")

    def get_name(self):
        return "1.1.15 Ensure pushing or merging of new code is restricted to specific individuals or teams (Manual)"

    def validate_specific(self, gl_group_project, gl_project) -> ControlResult:
        protected_branches = gl_project.protectedbranches.list(all=True)

        if len(protected_branches) == 0:
            return ControlResult(self.get_name(), False,
                                 f"Repository does not have protected branches!")

        passed = True
        more_info = ""

        for branch in protected_branches:
            merge_access_levels = branch.merge_access_levels

            for merge_access_level in merge_access_levels:
                merge_passed = merge_access_level.get('access_level') in self.allowed_merge_access_levels

                if not merge_passed:
                    passed = False
                    more_info += f"For branch: {branch.name} allowed to merge is: {merge_access_level.get('access_level_description')} but allowed should be Maintainers and Developers\n"

            push_access_levels = branch.push_access_levels
            for push_access_level in push_access_levels:
                push_passed = push_access_level.get('access_level') in self.allowed_push_access_levels

                if not push_passed:
                    passed = False
                    more_info += f"For branch: {branch.name} allowed to push is: {push_access_level.get('access_level_description')} but allowed should be no one\n"

        return ControlResult(self.get_name(), passed, more_info)
