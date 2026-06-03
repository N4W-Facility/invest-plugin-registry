import re


def construct_base_url(git_url, version):
    # Sanitize for safety:
    git_url = git_url.strip()
    version = version.strip()

    _, _, host, org, repo = re.sub(r'\.git$', '', git_url).split('/')

    if 'github.com' in host:
        return f"https://raw.githubusercontent.com/{org}/{repo}/refs/tags/{version}/FILENAME"

    return f"https://{host}/api/v4/projects/{org}%2F{repo}/repository/files/FILENAME/raw?ref={version}"
