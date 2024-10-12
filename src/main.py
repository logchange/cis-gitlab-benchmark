import argparse
import pprint

from src.common.get_token import get_gitlab_token
from src.common.logger import init_logger
from src.controls.code_changes.approval_dismissed import ApprovalDismissedControl
from src.controls.code_changes.approval_required import ApprovalRequiredControl
from src.controls.code_changes.codeowners_approval import CodeOwnersApprovalRequiredControl
from src.controls.code_changes.codeowners_file_exists import CodeOwnersFileExistsControl
from src.controls.code_changes.stale_branches import StaleBranchesRemovedControl
from src.export.xlsx_exporter import XlsxExporter
from src.projects import GitLabProjects

controls = [
    ApprovalRequiredControl(),
    ApprovalDismissedControl(),
    CodeOwnersFileExistsControl(),
    CodeOwnersApprovalRequiredControl(),
    StaleBranchesRemovedControl()
]


def check_controls(gitlab_group_project, gl_project):
    controls_result = []

    for control in controls:
        result = control.validate(gitlab_group_project, gl_project)
        controls_result.append(result)

    return {"name": gitlab_group_project.name, "url": gitlab_group_project.path_with_namespace, "controls_result": controls_result}


def start(group_name: str):
    print(f'CIS GitLab Benchmark')

    token = get_gitlab_token()
    init_logger(token)

    gl_projects = GitLabProjects(group_name)

    projects_list = gl_projects.get()

    project_results = []

    for project in projects_list:
        result = check_controls(project, gl_projects.get_project(project.id))
        project_results.append(result)

    pprint.pp(project_results)

    exporter = XlsxExporter()
    exporter.export(project_results, group_name)


def main():
    parser = argparse.ArgumentParser(description='CIS GitLab Benchmark')
    parser.add_argument('group_name', help='The group name to run this report on, f.e. gitlab-org')
    args = parser.parse_args()

    start(args.group_name)


if __name__ == '__main__':
    main()
