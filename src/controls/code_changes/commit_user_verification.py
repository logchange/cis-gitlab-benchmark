from gitlab import GitlabParsingError

from src.common.logger import warn
from src.controls.control import Control, ControlResult


class CommitUserVerificationControl(Control):

    def __init__(self, config: dict):
        control_dict = config.get('gitlab').get('code_changes').get('commit_user_verification')
        enabled = control_dict.get('enabled')
        super().__init__(enabled)
        self.reject_unsigned_commits_enabled = control_dict.get("reject_unsigned_commits")
        self.commit_committer_check_enabled = control_dict.get("commit_committer_check")
        self.commit_committer_name_check_enabled = control_dict.get("commit_committer_name_check")
        self.member_check_enabled = control_dict.get("member_check")

    def get_name(self):
        return "1.1.12 Ensure verification of signed commits for new changes before merging (Manual)"

    def validate_specific(self, gl_group_project, gl_project) -> ControlResult:
        try:
            rules = gl_project.pushrules.get()
        except GitlabParsingError as error:
            warn(error.error_message)
            return ControlResult(self.get_name(), False, "WARN Could not get info about push rules for this repo!")

        reject_unsigned_commits = rules.reject_unsigned_commits if self.reject_unsigned_commits_enabled else True  # Reject unsigned commits (original CIS GitLab v1.0.1)
        commit_committer_check = rules.commit_committer_check if self.commit_committer_check_enabled else True  # Reject unverified users
        commit_committer_name_check = rules.commit_committer_name_check if self.commit_committer_name_check_enabled else True  # Reject inconsistent user name
        member_check = rules.member_check if self.member_check_enabled else True  # Check whether the commit author is a GitLab user

        if reject_unsigned_commits and commit_committer_check and commit_committer_name_check and member_check:
            return ControlResult(self.get_name(), True, "")
        else:
            return ControlResult(self.get_name(), False, f"" +
                                 f"Push rules: \nReject unverified users: {commit_committer_check}\n" if self.commit_committer_check_enabled else "" +
                                 f"Reject inconsistent user name: {commit_committer_name_check}\n" if self.commit_committer_name_check_enabled else "" +
                                 f"Reject unsigned commits: {reject_unsigned_commits}\n" if self.reject_unsigned_commits_enabled else "" +
                                 f"Check whether the commit author is a GitLab user: {member_check}" if self.member_check_enabled else "")
