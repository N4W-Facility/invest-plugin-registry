"""Lint all metadata provided by the user.

Tests performed:
    * make sure all attributes are there in pyproject.toml

"""
# /// script
# requires-python = ">=3.6"
# dependencies = [
#     "packaging>=24.2",
#     "requests",
#     "validate_pyproject",
# ]
# ///
import argparse
import json
import re
import tomllib

import requests
import validate_pyproject.api  # requires packaging>=24.2 for enforcement.

ALLOWED_PLUGIN_TYPES = [
    'preprocessing', 'postprocessing', 'workflow', 'invest_model_variant',
    'new_model', 'other']


def _validate_pyproject_file(filepath):
    validator = validate_pyproject.api.Validator()
    with open(filepath, 'rb') as tomlfile:
        pyproject_data = tomllib.load(tomlfile)

    # Check for the standard pyproject.toml validation requirements
    try:
        validator(pyproject_data)
    except validate_pyproject.errors.ValidationError as error:
        return f"Could not load pyproject.toml: {error.message}"

    # Check for the plugins registry's requirements
    natcap_requirement_errors = []
    for attribute in ['Documentation', 'Issues', 'Repository']:
        if attribute not in pyproject_data['project']['urls']:
            natcap_requirement_errors.append(
                f'project.data block is missing the {attribute} attribute')
            continue
        req = requests.head(pyproject_data['project']['urls'][attribute])
        if not req.ok:
            natcap_requirement_errors.append(
                f'project.data.{attribute} could not be loaded')

    if natcap_requirement_errors:
        return (
            f"{filepath} was found to have validation errors:\n"
            + "\n".join(f"* {issue}" for issue in natcap_requirement_errors))

    return None


def _validate_project_json_file(filepath):
    try:
        with open(filepath, 'r') as project_json:
            json_data = json.load(project_json)
    except json.decoder.JSONDecodeError as error:
        return f"Could not parse JSON file at {filepath}: {str(error)}"

    # We're assuming that the top-level object is an array
    issues = []
    for object_num, plugin_data in enumerate(json_data):
        if "repo_url" in plugin_data:
            url = plugin_data['repo_url']
            req = requests.head(url)
            if not req.ok:
                issues.append(f"URL {url} could not be found")
        else:
            issues.append(
                f"Plugin {object_num} is missing the attribute 'repo_url'")

        if "version" in plugin_data:
            if not re.match('^[0-9]+.[0-9]+.[0-9]+$',
                            str(plugin_data['version'])):
                issues.append(
                    "Version string must be in the form MAJOR.MINOR.PATCH")
        else:
            issues.append(
                f"Plugin {object_num} is missing the attribute 'version'")

        if 'plugin_type' in plugin_data:
            plugin_type = plugin_data['plugin_type']
            if plugin_type not in ALLOWED_PLUGIN_TYPES:
                issues.append(
                    f"Plugin type '{plugin_type}' must be one of the "
                    f'supported plugin types {ALLOWED_PLUGIN_TYPES}')
        else:
            issues.append(
                f"Plugin {object_num} is missing the attribute 'plugin_type'")

        # We don't have any requirements about keywords at this time, so
        # skipping any validation except for existence of the attribute.
        if 'keywords' not in plugin_data:
            issues.append(
                f"Plugin {object_num} is missing the attribute 'keywords'")

    if issues:
        return (
            f"{filepath} was found to have some formatting issues:\n"
            + "\n".join(f"* {issue}" for issue in issues))
    return None


def main(args=None):
    parser = argparse.ArgumentParser(
        "lint-metadata.py", description=())
    parser.add_argument('PYPROJECT_TOML_FILE', help="path to a pyproject.toml file")
    parser.add_argument('PLUGIN_JSON_FILE',
                        help="path to the plugin.json file")
    parser.add_argument(
        '--target-file',
        default=None,
        help=("Where output should be written. If not provided, output is "
              "written to stdout"))

    parsed_args = parser.parse_args(args)

    # Restart the file so we can append to it later.
    if parsed_args.target_file is not None:
        with open(parsed_args.target_file, 'w'):
            pass

    def _write_to_file(possible_string):
        if possible_string is None:
            return

        if parsed_args.target_file is None:
            print(possible_string)
        else:
            with open(parsed_args.target_file, 'a') as target_file:
                target_file.write(possible_string)

    pyproject_errors = _validate_pyproject_file(parsed_args.PYPROJECT_TOML_FILE)
    json_errors = _validate_project_json_file(parsed_args.PLUGIN_JSON_FILE)
    _write_to_file(pyproject_errors)
    _write_to_file(json_errors)

    if (pyproject_errors is None and json_errors is None):
        _write_to_file("No errors found in the project!")
    else:
        parser.error("Linting errors found")


if __name__ == '__main__':
    main()
