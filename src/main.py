import argparse

from src.common.get_token import get_gitlab_token
from src.common.logger import init_logger
from src.controls.code_changes.approval_dismissed import ApprovalDismissedControl
from src.controls.code_changes.approval_required import ApprovalRequiredControl
from src.controls.code_changes.codeowners_approvals import CodeOwnersApprovalControl
from src.projects import GitLabProjects

controls = [
    ApprovalRequiredControl(),
    ApprovalDismissedControl(),
    CodeOwnersApprovalControl()
]


def check_controls(gitlab_group_project, gl_project):
    for control in controls:
        result = control.validate(gitlab_group_project, gl_project)
        # TODO


def start(group_name: str):
    print(f'CIS GitLab Benchmark')

    token = get_gitlab_token()
    init_logger(token)

    gl_projects = GitLabProjects(group_name)

    projects_list = gl_projects.get()

    for project in projects_list:
        check_controls(project, gl_projects.get_project(project.id))


def main():
    parser = argparse.ArgumentParser(description='CIS GitLab Benchmark')
    parser.add_argument('group_name', help='The group name to run this report on, f.e. gitlab-org')
    args = parser.parse_args()

    start(args.group_name)


if __name__ == '__main__':
    main()
