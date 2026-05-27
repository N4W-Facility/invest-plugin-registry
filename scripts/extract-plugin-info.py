import argparse
import textwrap
import tomllib


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "pyproject_toml", help="Path to config file"
    )
    parser.add_argument(
        "target_markdown", help="Path to target output markdown file"
    )
    args = parser.parse_args()

    with open(args.pyproject_toml) as f:
        config = tomllib.load(f)

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

    with open(args.target_markdown, 'w') as target_file:
        target_file.write(textwrap.dedent(
            f"""\
            ### Metadata pulled from `pyproject.toml`

            *Plugin name*: {project_name}
            *Version*: `pyproject.toml`: {version}
            *License*: {license}
            *Documentation*: {docs}

            *Description*

            {description}

        """))


if __name__ == "__main__":
    main()
