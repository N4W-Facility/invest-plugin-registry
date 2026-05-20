"""Collect and repackage project metadata."""
import argparse
import bz2
import datetime
import hashlib
import json
import logging
import os
import re
import shutil
import tomllib

import requests

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
REPO_ROOT = os.path.join(os.path.dirname(__file__), '..')
DEFAULT_PLUGINS_FILE = os.path.join(REPO_ROOT, 'plugins.json')
DEFAULT_OUTDIR = os.path.join(REPO_ROOT, 'html')

DESCRIPTION_OUTDIR = os.path.join(REPO_ROOT, 'source', 'plugins', 'partials')


def _hashfile(filepath):
    sha = hashlib.sha256()
    with open(filepath, 'rb') as opened_file:
        while True:
            data = opened_file.read(512)
            if not data:
                break
            sha.update(data)
    return sha.hexdigest()


def _version_info(host, org, repo, version):
    if 'github.com' in host:
        resp = requests.get(
            f'https://api.github.com/repos/{org}/{repo}/git/refs/tags/{version}')
        tag_json = resp.json()
        resp = requests.get(tag_json['object']['url'])
        version_json = resp.json()
        sha = version_json['sha']
        date = version_json['author']['date']
    else:
        resp = requests.get(
            f'https://{host}/api/v4/projects/{org}%2F{repo}/repository/tags/{version}')
        tag_json = resp.json()
        sha = tag_json['commit']['id']
        date = tag_json['created_at']
    return sha, date


def _construct_url(host, org, repo, version):
    if 'github.com' in host:
        base_api_url = f"https://raw.githubusercontent.com/{org}/{repo}/refs/tags/{version}/FILENAME"

    else:
        base_api_url = f"https://{host}/api/v4/projects/{org}%2F{repo}/repository/files/FILENAME/raw?ref={version}"

    return base_api_url


def main(args=None):
    parser = argparse.ArgumentParser("collect-metadata.py")
    parser.add_argument('--pluginslist', default=DEFAULT_PLUGINS_FILE,
                        required=False)
    parser.add_argument('--outdir', default=DEFAULT_OUTDIR, required=False)

    parsed_args = parser.parse_args(args)

    outdir = os.path.normpath(parsed_args.outdir)
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    if not os.path.exists(DESCRIPTION_OUTDIR):
        os.makedirs(DESCRIPTION_OUTDIR)

    all_toml_data = {}  # name: loaded_toml
    with open(parsed_args.pluginslist, 'r') as plugins_list:
        plugins_json = json.load(plugins_list)

    for plugin in plugins_json:
        plugin_git_url = plugin['repo_url'].strip()
        plugin_version = plugin['version'].strip()
        LOGGER.info(f"Processing {plugin_git_url}, version {plugin_version}")

        _, _, host, org, repo = re.sub(r'\.git$', '', plugin_git_url).split('/')

        base_url = _construct_url(host, org, repo, plugin_version)

        pyproject_url = base_url.replace('FILENAME', 'pyproject.toml')
        LOGGER.debug(f"Getting toml {pyproject_url}")

        resp = requests.get(pyproject_url)
        pyproject_toml = tomllib.loads(resp.text)
        project_name = pyproject_toml['project']['name']

        description_partial = None
        description_file = pyproject_toml['tool']['natcap']['invest'].get(
                           'registry_description')
        if description_file:
            description_url = base_url.replace('FILENAME', description_file.strip('/'))
            LOGGER.info(f"Getting description file {description_url}")
            resp = requests.get(description_url)
            if resp.ok:
                description_outpath = os.path.join(DESCRIPTION_OUTDIR,
                    f'{project_name}{os.path.splitext(description_file)[-1]}')
                with open(description_outpath, 'w') as f:
                    f.write(resp.text)
                description_partial = f'{os.path.basename(description_outpath)}'
            else:
                LOGGER.warning(
                    f"The description file {description_url} returned "
                    f"non-OK status code {resp.status_code}")

        commit_sha, tag_date = _version_info(host, org, repo, plugin_version)
        all_toml_data[project_name] = {
            'pyproject_toml': pyproject_toml,
            'github_repo': plugin_git_url,
            'version': plugin_version,
            'current_commit_sha': commit_sha,
            'date_last_updated': tag_date,
            'plugin_type': plugin['plugin_type'],
            'keywords': plugin['keywords'],
            'description_path': description_partial
        }

    metadata_object = {
        'data': all_toml_data,
        'generated': datetime.datetime.today().isoformat(),
        'schema_version': 0,  # in case we need a new version of this
    }

    metadata_json_path = os.path.join(outdir, 'metadata.json')
    LOGGER.info(f"Writing {metadata_json_path}")
    with open(metadata_json_path, 'w') as metadata_json_file:
        json.dump(metadata_object, metadata_json_file)

    LOGGER.info(f"Writing {metadata_json_path}.sha256")
    with open(f'{metadata_json_path}.sha256', 'w') as metadata_sha256:
        metadata_sha256.write(_hashfile(metadata_json_path))

    # Using bzip2 here because that's what conda-forge uses and seems
    # reasonable.  Not sure if it's strictly necessary if the github pages
    # webserver already has gzip compression enabled.
    LOGGER.info(f'Writing {metadata_json_path}.bz2')
    with open(metadata_json_path, 'rb') as metadata_in:
        with bz2.open(f'{metadata_json_path}.bz2', 'wb') as metadata_out:
            shutil.copyfileobj(metadata_in, metadata_out)

    LOGGER.info(f'Writing {metadata_json_path}.bz2.sha256')
    with open(f'{metadata_json_path}.bz2.sha256', 'w') as metadata_sha256:
        metadata_sha256.write(_hashfile(f'{metadata_json_path}.bz2'))


if __name__ == '__main__':
    main()
