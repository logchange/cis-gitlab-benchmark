import os

from src.common.get_token import get_valhalla_token
from src.common.logger import info
import gitlab


def get_gitlab_client():
    protocol = os.getenv("CI_SERVER_PROTOCOL")
    host = os.getenv("CI_SERVER_HOST")
    port = os.getenv("CI_SERVER_PORT")

    gitlab_url = f"{protocol}://{host}:{port}"
    info("GitLab URL: " + gitlab_url)

    token = get_valhalla_token()

    gl = gitlab.Gitlab(gitlab_url, oauth_token=token)
    return gl
