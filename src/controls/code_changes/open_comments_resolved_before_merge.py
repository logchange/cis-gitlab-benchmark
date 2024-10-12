from src.controls.control import Control, ControlResult


class AllOpenCommentsAreResolvedBeforeControl(Control):
    def get_name(self):
        return "1.1.11 Ensure all open comments are resolved before allowing code change merging (Manual)"

    def validate(self, gl_group_project, gl_project) -> ControlResult:
        all_comments = gl_project.only_allow_merge_if_all_discussions_are_resolved

        if all_comments:
            return ControlResult(self.get_name(), True, "")
        else:
            return ControlResult(self.get_name(), False, f"All threads must be resolved: {all_comments}")
