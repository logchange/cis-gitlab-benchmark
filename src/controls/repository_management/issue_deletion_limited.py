from src.common.logger import info
from src.controls.control import Control, ControlResult


class IssueDeletionLimitedControl(Control):
    DELETION_ACCESS_LEVEL = [50, 60]

    def __init__(self, config: dict):
        control_dict = config.get('gitlab').get('repository_management').get('issue_deletion_limited')
        enabled = control_dict.get('enabled')
        super().__init__(enabled)
        self.max_number_of_users_allowed_to_delete_issue = control_dict.get("max_number_of_users_allowed_to_delete_issue")

    def get_name(self):
        return "1.2.4 Ensure issue deletion is limited to specific users (Manual)"

    def validate_specific(self, gl_group_project, gl_project) -> ControlResult:
        members = gl_project.members_all.list(all=True)

        counter = 0
        users_allowed_to_delete = f"Exceeded number of {self.max_number_of_users_allowed_to_delete_issue} users\nMembers allowed to delete issue:\n"

        for member in members:
            if member.access_level in self.DELETION_ACCESS_LEVEL:
                counter += 1
                users_allowed_to_delete = f"- ({member.username}){member.name}\n"

        if counter <= self.max_number_of_users_allowed_to_delete_issue:
            return ControlResult(self.get_name(), True, f"Number of users able to delete issue: {counter}")
        else:
            return ControlResult(self.get_name(), False, f"Number of users able to delete issue: {counter}\n{users_allowed_to_delete}")
