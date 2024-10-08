import os

from src.common.logger import info, error


def get_gitlab_token() -> str:
    token = os.getenv('GITLAB_TOKEN')

    if token:
        info(f'Variable GITLAB_TOKEN is set to: {"*" * len(token)}')

        return token
    else:
        error('GITLAB_TOKEN environment variable is not set! \n' +
              'This tool cannot be used if there is no token! \n' +
              'Please generate token (f.e. Personal Access Token) \n' +
              'and add it as environment variable with name GITLAB_TOKEN')
        exit(-1)
