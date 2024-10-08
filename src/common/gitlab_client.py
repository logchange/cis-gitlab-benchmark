import os

import gitlab

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
