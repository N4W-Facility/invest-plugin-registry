import argparse
import json
import logging
import os
import re
import textwrap

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


PLUGIN_TYPES = {
    "preprocessing": "Preprocessing",
    "postprocessing": "Postprocessing",
    "workflow": "Workflow",
    "invest_model_variant": "InVEST Model Variant",
    "new_model": "New Model",
    "other": "Other"
}


def format_contact(contacts):
    contacts_list = []
    for contact in contacts:
        name = contact.get('name')
        email = contact.get('email')
        if not name and not email:
            pass
        if name and email:
            contacts_list.append(f"{name} ({email})")
        else:
            contacts_list.append(f"{name or email}")
    contacts_str = "; ".join(contacts_list)
    return contacts_str


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
        # only list as pypi deps those packages that are not listed in conda
        # deps
        if '\n' in condaforge_dependencies:
            cf_pkgs = set([re.findall('^\w+', dep)[0] for dep in
                           cf_dependencies_list])
            pypi_dependencies_list = []
            for pypi_dep in pypi_deps_list:
                pkg = re.findall('^\w+', pypi_dep)[0]
                if pkg not in cf_pkgs:
                    pypi_dependencies_list.append(pypi_dep)
            pypi_dependencies = "\n".join(
                [" "*12 + dep for dep in pypi_dependencies_list])
        else:
            pypi_dependencies = "\n".join(
                [" "*12 + dep for dep in pypi_deps_list]).lstrip()

    else:
        pypi_dependencies = "No PyPI dependencies defined"

    repo_url = re.sub(r'\.git$', '', plugin_metadata['github_repo']).rstrip('/')
    issues_link = plugin_metadata['pyproject_toml']['project']['urls'].get(
            'Issues', f"{repo_url}/issues")
    docs_link = plugin_metadata['pyproject_toml']['project']['urls'].get(
            'Documentation', repo_url)
    if not docs_link.startswith('http'):
        # Assume it's a filepath relative to the root of the repo
        docs_link = f"{repo_url}/{docs_link.lstrip('/')}"

    # Template partial for authors / maintainers; construct separately
    # since only one may be included
    maintainers = plugin_metadata['pyproject_toml']['project'].get('maintainers')
    authors = plugin_metadata['pyproject_toml']['project'].get('authors')
    if authors or maintainers:
        authors_str = maintainers_str = None
        if maintainers:
            maintainers_str = "**Maintainers:** " + format_contact(maintainers)
        if authors:
            authors_str = "**Authors:** " + format_contact(authors)

        if authors and maintainers:
            authors_maintainers = (
                f"""
                | {authors_str}
                | {maintainers_str}
                |
                """)
        else:
            authors_maintainers = (
                f"""
                | {authors_str or maintainers_str}
                |
                """)
    else:
        authors_maintainers = (
            """
            |
            """)

    # Description handling
    if plugin_metadata['description_path']:
        if plugin_metadata['description_path'].lower().endswith(('md', 'txt')):
            parser = 'myst'
        else:
            parser = 'rst'
        description_partial = (f"""
        .. include:: partials/{plugin_metadata['description_path']}
           :parser: {parser}
        """)
    else:
        description_partial = (f"""
        About
        -----

        {project_description}
        """)

    # Construct the template
    template_start = (
        f"""
        {project_name}
        {'='*len(project_name)}

        .. info-card::

            .. grid-item::
                :columns: 12

                | **Source Code:** {plugin_metadata['github_repo']}
                | **Current Version:** {plugin_metadata['version']}
                | **Last Updated:** {plugin_metadata['date_last_updated']}
                |
        """)

    template_end = (
        f"""
                | `Documentation <{docs_link}>`_ :octicon:`link-external` | `Issue Tracker <{issues_link}>`_ :octicon:`link-external`
                |

                :tags-primary:`{PLUGIN_TYPES.get(plugin_metadata['plugin_type'], 'Unknown')}`
                :tags-info:`{','.join(tag for tag in plugin_metadata['keywords'])}`

        {description_partial}

        Dependencies
        ------------

        This plugin will pull these dependencies from PyPI::

            {pypi_dependencies}

        And these dependencies will be pulled from conda-forge::

            {condaforge_dependencies}

        """)

    template = textwrap.dedent(template_start + authors_maintainers + template_end)

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
