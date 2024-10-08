class ControlResult:

    def __init__(self, passed: bool, more_info: str):
        self.passed = passed
        self.more_info = more_info


class Control:

    def get_name(self):
        raise NotImplementedError("You have to implement get_name method!")

    def validate(self, gitlab_group_project, gl_project) -> ControlResult:
        raise NotImplementedError("You have to implement validate method!")
