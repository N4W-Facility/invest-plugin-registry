import argparse
import json
import textwrap
import tomllib

from utils import construct_base_url


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "pyproject_toml", help="Path to config file"
    )
    parser.add_argument(
        "plugin_json", help="Path to the plugin.json file"
    )
    parser.add_argument(
        "target_markdown", help="Path to target output markdown file"
    )
    args = parser.parse_args()

    with open(args.pyproject_toml, 'rb') as f:
        config = tomllib.load(f)

    with open(args.plugin_json, "r") as f:
        plugin_data = json.load(f)

    try:
        project_name = config['project']['name']
    except KeyError:
        project_name = "UNDEFINED"

    try:
        version = config['project']['version']
    except KeyError:
        version = "see pyproject.toml; might be dynamic"

    try:
        license = config['project']['license']
    except KeyError:
        license = "UNDEFINED"

    try:
        description = config['project']['description']
    except KeyError:
        description = "UNDEFINED"

    try:
        docs = config['project']['urls']['Documentation']
    except KeyError:
        docs = "UNDEFINED"

    try:
        description_file = config['tool']['natcap']['invest']['registry_description']
    except KeyError:
        description_file = None

    if description_file:
        base_url = construct_base_url(plugin_data['repo_url'], plugin_data['version'])
        description_link = base_url.replace('FILENAME', description_file.strip('/'))
    else:
        description_link = ("No registry description file provided; "
                            "project description will be used")

    with open(args.target_markdown, 'w') as target_file:
        target_file.write(textwrap.dedent(
            f"""\n
            ### Metadata pulled from `pyproject.toml`

            *Project name*: {project_name}
            *Plugin display name*: {plugin_data['plugin_name']}
            *Version*: `pyproject.toml`: {version}
            *License*: {license}
            *Documentation*: {docs}
            *Registry description link*: {description_link}

            *Project description*

            {description}

        """))


if __name__ == "__main__":
    main()
