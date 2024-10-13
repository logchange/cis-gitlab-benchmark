from src.common.logger import info
from src.controls.control import Control, ControlResult


class IssueDeletionLimitedControl(Control):
    DELETION_ACCESS_LEVEL = [50, 60]

    MAX_NUMBER_OF_ALLOWED_TO_DELETE_ISSUE = 10

    def get_name(self):
        return "1.2.4 Ensure issue deletion is limited to specific users (Manual)"

    def validate(self, gl_group_project, gl_project) -> ControlResult:
        info(f"Project name: {gl_project.name} - Performing check {self.get_name()}")

        members = gl_project.members_all.list(all=True)

        counter = 0
        users_allowed_to_delete = f"Exceeded number of {self.MAX_NUMBER_OF_ALLOWED_TO_DELETE_ISSUE} users\nMembers allowed to delete issue:\n"

        for member in members:
            if member.access_level in self.DELETION_ACCESS_LEVEL:
                counter += 1
                users_allowed_to_delete = f"- ({member.username}){member.name}\n"

        if counter <= self.MAX_NUMBER_OF_ALLOWED_TO_DELETE_ISSUE:
            return ControlResult(self.get_name(), True, f"Number of users able to delete issue: {counter}")
        else:
            return ControlResult(self.get_name(), False, f"Number of users able to delete issue: {counter}\n{users_allowed_to_delete}")
