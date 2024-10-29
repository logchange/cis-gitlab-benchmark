import os
from numbers import Number

import gitlab
from gitlab import GitlabHttpError

from src.common.get_token import get_gitlab_token
from src.common.logger import info


def get_gitlab_client():
    url = os.getenv("GITLAB_URL")

    if url:
        gitlab_url = url
    else:
        protocol = os.getenv("CI_SERVER_PROTOCOL")
        host = os.getenv("CI_SERVER_HOST")
        port = os.getenv("CI_SERVER_PORT")
        gitlab_url = f"{protocol}://{host}:{port}"

    info("GitLab URL: " + gitlab_url)

    token = get_gitlab_token()

    gl = gitlab.Gitlab(gitlab_url, oauth_token=token)
    return gl


def file_exists(gl_project, file_name: str) -> Number | None:
    try:
        id = [d['id'] for d in gl_project.repository_tree() if d['name'] == file_name][0]
        return True
    except IndexError:
        return False
    except Exception as e:
        info(str(e))
        return False
