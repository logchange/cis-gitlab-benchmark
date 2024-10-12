from src.common.logger import info
from src.controls.control import Control, ControlResult


class CommitUserVerificationControl(Control):
    def get_name(self):
        return "1.1.12 Ensure verification of signed commits for new changes before merging (Manual)"

    def validate(self, gl_group_project, gl_project) -> ControlResult:
        info(f"Project name: {gl_project.name} - Performing check {self.get_name()}")

        rules = gl_project.pushrules.get()

        reject_unsigned_commits = rules.reject_unsigned_commits  # Reject unsigned commits (original CIS GitLab v1.0.1)
        commit_committer_check = rules.commit_committer_check  # Reject unverified users
        commit_committer_name_check = rules.commit_committer_name_check  # Reject inconsistent user name
        member_check = rules.member_check  # Check whether the commit author is a GitLab user

        if reject_unsigned_commits and commit_committer_check and commit_committer_name_check and member_check:
            return ControlResult(self.get_name(), True, "")
        else:
            return ControlResult(self.get_name(), False, f"" +
                                 f"Push rules: \nReject unverified users: {commit_committer_check}\n" +
                                 f"Reject inconsistent user name: {commit_committer_name_check}\n" +
                                 f"Reject unsigned commits: {reject_unsigned_commits}\n" +
                                 f"Check whether the commit author is a GitLab user: {member_check}")
