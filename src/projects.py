from src.common.gitlab_client import get_gitlab_client


class GitLabProjects:
    def __init__(self, group_name: str):
        self.gl = get_gitlab_client()
        self.group_name = group_name

    def get(self):
        group_object = self.gl.groups.get(self.group_name)
        group_projects = group_object.projects.list(as_list=False,
                                                    include_subgroups=True,
                                                    get_all=True,
                                                    # per_page=2, # only for test purposes
                                                    archived=False,
                                                    with_shared=False,
                                                    simple=False,)

        return group_projects

    def get_project(self, project_id):
        return self.gl.projects.get(project_id, lazy=False)
