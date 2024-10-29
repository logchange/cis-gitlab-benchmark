from src.common.logger import info


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

    def __init__(self, enabled: bool):
        self.enabled = enabled

    def get_name(self):
        raise NotImplementedError("You have to implement get_name method!")

    def validate_specific(self, gl_group_project, gl_project) -> ControlResult:
        raise NotImplementedError("You have to implement validate_specific method!")

    def validate(self, gitlab_group_project, gl_project) -> ControlResult | None:
        if not self.enabled:
            info(f"Project name: {gl_project.name} - Skipping performing check {self.get_name()}")
            return None

        info(f"Project name: {gl_project.name} - Performing check {self.get_name()}")

        return self.validate_specific(gitlab_group_project, gl_project)


