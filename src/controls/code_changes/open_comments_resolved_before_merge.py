from src.common.logger import info
from src.controls.control import Control, ControlResult


class AllOpenCommentsAreResolvedBeforeControl(Control):
    
    def __init__(self, config: dict):
        control_dict = config.get('gitlab').get('code_changes').get('open_comments_resolved_before_merge')
        enabled = control_dict.get('enabled')
        super().__init__(enabled)
    
    def get_name(self):
        return "1.1.11 Ensure all open comments are resolved before allowing code change merging (Manual)"

    def validate_specific(self, gl_group_project, gl_project) -> ControlResult:
        all_comments = gl_project.only_allow_merge_if_all_discussions_are_resolved

        if all_comments:
            return ControlResult(self.get_name(), True, "")
        else:
            return ControlResult(self.get_name(), False, f"All threads must be resolved: {all_comments}")
