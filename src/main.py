import argparse
import pprint

from src.common.get_token import get_gitlab_token
from src.common.logger import init_logger
from src.config.config import get_config
from src.controls.code_changes.approval_dismissed import ApprovalDismissedControl
from src.controls.code_changes.approval_required import ApprovalRequiredControl
from src.controls.code_changes.branch_deletion_denied import BranchDeletionDeniedControl
from src.controls.code_changes.branches_are_up_to_date import BranchesAreUpToDateControl
from src.controls.code_changes.checks_have_passed_before_merging import AllChecksHavePassedBeforeMergingControl
from src.controls.code_changes.codeowners_approval import CodeOwnersApprovalRequiredControl
from src.controls.code_changes.codeowners_file_exists import CodeOwnersFileExistsControl
from src.controls.code_changes.commit_user_verification import CommitUserVerificationControl
from src.controls.code_changes.default_branch_protected import DefaultBranchProtectedControl
from src.controls.code_changes.force_push_denied import ForcePushDeniedControl
from src.controls.code_changes.linear_history import LinearHistoryControl
from src.controls.code_changes.open_comments_resolved_before_merge import AllOpenCommentsAreResolvedBeforeControl
from src.controls.code_changes.pushing_or_merging_restriction import PushingOrMergingRestrictionControl
from src.controls.code_changes.stale_branches import StaleBranchesRemovedControl
from src.controls.repository_management.inactive_repositories import RepositoryInactivityControl
from src.controls.repository_management.issue_deletion_limited import IssueDeletionLimitedControl
from src.controls.repository_management.repository_deletion_limited import RepositoryDeletionLimitedControl
from src.controls.repository_management.repository_forks import RepositoryForksControl
from src.controls.repository_management.security_file_available import SecurityFileExistsControl
from src.export.xlsx_exporter import XlsxExporter
from src.projects import GitLabProjects


def get_controls(config: dict):
    return [
        ApprovalRequiredControl(config),
        ApprovalDismissedControl(config),
        CodeOwnersFileExistsControl(config),
        CodeOwnersApprovalRequiredControl(config),
        StaleBranchesRemovedControl(config),
        AllChecksHavePassedBeforeMergingControl(config),
        BranchesAreUpToDateControl(config),
        AllOpenCommentsAreResolvedBeforeControl(config),
        CommitUserVerificationControl(config),
        LinearHistoryControl(config),
        PushingOrMergingRestrictionControl(config),
        ForcePushDeniedControl(config),
        BranchDeletionDeniedControl(config),
        DefaultBranchProtectedControl(config),
        SecurityFileExistsControl(config),
        RepositoryDeletionLimitedControl(config),
        IssueDeletionLimitedControl(config),
        RepositoryForksControl(config),
        RepositoryInactivityControl(config)
    ]


def check_controls(controls, gitlab_group_project, gl_project):
    controls_result = []

    for control in controls:
        result = control.validate(gitlab_group_project, gl_project)

        if result is not None:
            controls_result.append(result)

    return {"name": gitlab_group_project.name, "url": gitlab_group_project.path_with_namespace,
            "controls_result": controls_result}


def start(group_name: str, config_path: str):
    print(f'CIS GitLab Benchmark')

    token = get_gitlab_token()
    init_logger(token)

    config = get_config(config_path)
    controls = get_controls(config)

    gl_projects = GitLabProjects(group_name)

    projects_list = gl_projects.get()

    project_results = []

    for project in projects_list:
        result = check_controls(controls, project, gl_projects.get_project(project.id))
        project_results.append(result)

    pprint.pp(project_results)

    exporter = XlsxExporter()
    exporter.export(project_results, group_name)


def main():
    parser = argparse.ArgumentParser(description='CIS GitLab Benchmark')
    parser.add_argument('group_name', help='The group name to run this report on, f.e. gitlab-org')
    parser.add_argument('config', help='Path to the config file, f.e. config.yml')

    args = parser.parse_args()

    start(args.group_name, args.config)


if __name__ == '__main__':
    main()
