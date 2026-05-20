"""Collect and repackage project metadata."""
import argparse
import bz2
import datetime
import hashlib
import json
import logging
import os
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


def _version_info(owner, repo, version):
    resp = requests.get(
        f'https://api.github.com/repos/{owner}/{repo}/git/refs/tags/{version}')
    resp.raise_for_status()
    tag_json = resp.json()
    resp = requests.get(tag_json['object']['url'])
    resp.raise_for_status()
    return resp.json()


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
        user, repo = plugin_git_url.replace(
            'https://github.com/', '').replace('.git', '').split('/')

        base_url = (
            f'https://raw.githubusercontent.com/{user}/{repo}'
            f'/refs/tags/{plugin_version}')

        pyproject_url = f'{base_url}/pyproject.toml'
        LOGGER.debug(f"Getting toml {pyproject_url}")

        resp = requests.get(pyproject_url)
        pyproject_toml = tomllib.loads(resp.text)
        project_name = pyproject_toml['project']['name']

        description_partial = None
        description_file = pyproject_toml['tool']['natcap']['invest'].get(
                           'registry_description')
        if description_file:
            description_url = f"{base_url}/{description_file.strip('/')}"
            LOGGER.info(f"Getting description file {description_url}")
            resp = requests.get(description_url)
            if resp.ok:
                description_outpath = os.path.join(DESCRIPTION_OUTDIR,
                    f'{project_name}{os.path.splitext(description_url)[-1]}')
                with open(description_outpath, 'w') as f:
                    f.write(resp.text)
                description_partial = f'{os.path.basename(description_outpath)}'

        version_data = _version_info(user, repo, plugin_version)
        all_toml_data[project_name] = {
            'pyproject_toml': pyproject_toml,
            'github_repo': plugin_git_url,
            'version': plugin_version,
            'current_commit_sha': version_data['sha'],
            'date_last_updated': version_data['author']['date'],
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
