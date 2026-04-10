import argparse
import json
import logging
import os
import textwrap

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def render_rst_file(plugin_name, plugin_metadata, out_dir):

    try:
        project_name = plugin_metadata[
            'pyproject_toml']['project']['name']
        if not project_name:  # guard against empty string
            raise KeyError()
    except KeyError:
        project_name = plugin_name

    try:
        project_description = plugin_metadata[
            'pyproject_toml']['project']['description']
        if not project_description:
            raise KeyError
    except KeyError:
        project_description = (
            "*This project did not provide a description in its package "
            "configuration, defined in* ``pyproject.toml``.")

    cf_dependencies_list = plugin_metadata[
        'pyproject_toml']['tool']['natcap']['invest']['conda_dependencies']
    if cf_dependencies_list:
        condaforge_dependencies = "\n".join([" "*12 + dep for dep in cf_dependencies_list]).lstrip()
    else:
        condaforge_dependencies = "No conda-forge dependencies defined"

    pypi_deps_list = plugin_metadata[
        'pyproject_toml']['project']['dependencies']
    if pypi_deps_list:
        pypi_dependencies = "\n".join(
            [" "*12 + dep for dep in pypi_deps_list]).lstrip()
    else:
        pypi_dependencies = "No PyPI dependencies defined"

    template = textwrap.dedent(
        f"""
        {project_name}
        {'='*len(project_name)}

        {project_description}

        * Last updated: {plugin_metadata['date_last_updated']}
        * Source code: {plugin_metadata['github_repo']}

        Dependencies
        ------------

        This plugin will pull these dependencies from PyPI::

            {pypi_dependencies}

        And these dependencies will be pulled from conda-forge::

            {condaforge_dependencies}

        """)

    out_filename = os.path.join(out_dir, f'{plugin_name}.rst')
    with open(out_filename, 'w') as out_file:
        out_file.write(template)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('metadata')
    parser.add_argument('outdir')

    parsed_args = parser.parse_args()

    with open(parsed_args.metadata, 'r') as metadata_file:
        parsed_json = json.load(metadata_file)

    for plugin_name, plugin_data in parsed_json['data'].items():
        LOGGER.info(f"Writing out RSN for {plugin_name}")
        render_rst_file(plugin_name, plugin_data, parsed_args.outdir)


if __name__ == '__main__':
    main()
