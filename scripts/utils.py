import re
from urllib.parse import urlparse


def construct_base_url(git_url, version):
    # Sanitize for safety:
    git_url = git_url.strip()
    version = version.strip()

    normalized_url = re.sub(r'\.git$', '', git_url)
    parsed = urlparse(normalized_url)
    host = parsed.hostname or ''
    path_parts = parsed.path.strip('/').split('/')
    org, repo = path_parts[0], path_parts[1]

    if host == 'github.com':
        return f"https://raw.githubusercontent.com/{org}/{repo}/refs/tags/{version}/FILENAME"

    return f"https://{host}/api/v4/projects/{org}%2F{repo}/repository/files/FILENAME/raw?ref={version}"
