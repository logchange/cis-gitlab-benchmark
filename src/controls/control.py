class ControlResult:

    def __init__(self, control_name: str, passed: bool, more_info: str):
        self.control_name = control_name
        self.passed = passed
        self.more_info = more_info

    def to_dict(self):
        return vars(self)

    def __repr__(self):
        return str(self.to_dict())


class Control:

    def get_name(self):
        raise NotImplementedError("You have to implement get_name method!")

    def validate(self, gitlab_group_project, gl_project) -> ControlResult:
        raise NotImplementedError("You have to implement validate method!")
