from src.common.logger import info
from src.controls.control import Control, ControlResult


class PushingOrMergingRestrictionControl(Control):

    # https://docs.gitlab.com/ee/api/access_requests.html
    ALLOWED_MERGE_ACCESS_LEVELS = [30, 40]  # 30 - Developers + Maintainers, 40 - Maintainers
    ALLOWED_PUSH_ACCESS_LEVELS = [0]  # 0 - No one

    def get_name(self):
        return "1.1.15 Ensure pushing or merging of new code is restricted to specific individuals or teams (Manual)"

    def validate(self, gl_group_project, gl_project) -> ControlResult:
        info(f"Project name: {gl_project.name} - Performing check {self.get_name()}")

        protected_branches = gl_project.protectedbranches.list(all=True)

        if len(protected_branches) == 0:
            return ControlResult(self.get_name(), False,
                                 f"Repository does not have protected branches!")

        passed = True
        more_info = ""

        for branch in protected_branches:
            merge_access_levels = branch.merge_access_levels

            for merge_access_level in merge_access_levels:
                merge_passed = merge_access_level.get('access_level') in self.ALLOWED_MERGE_ACCESS_LEVELS

                if not merge_passed:
                    passed = False
                    more_info += f"For branch: {branch.name} allowed to merge is: {merge_access_level.get('access_level_description')} but allowed should be Maintainers and Developers\n"

            push_access_levels = branch.push_access_levels
            for push_access_level in push_access_levels:
                push_passed = push_access_level.get('access_level') in self.ALLOWED_PUSH_ACCESS_LEVELS

                if not push_passed:
                    passed = False
                    more_info += f"For branch: {branch.name} allowed to push is: {push_access_level.get('access_level_description')} but allowed should be no one\n"

        return ControlResult(self.get_name(), passed, more_info)
