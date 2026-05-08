"""Lint all metadata provided by the user.

Tests performed:
    * make sure all attributes are there in pyproject.toml
    *

"""
import argparse
import tomllib

import requests
import validate_pyproject


def _validate_pyproject_file(filepath):
    validator = validate_pyproject.api.Validator()
    with open(filepath, 'r') as tomlfile:
        pyproject_data = tomllib.load(tomlfile)

    # Check for the standard pyproject.toml validation requirements
    try:
        validator.validator(pyproject_data)
    except validate_pyproject.errors.ValidationError as error:
        return f"Could not load pyproject.toml: {error.message}"

    # Check for the plugins registry's requirements
    natcap_requirement_errors = []
    for attribute in ['Documentation', 'Issues', 'Repository']:
        if attribute not in pyproject_data['project']['data']:
            natcap_requirement_errors.append(
                f'project.data block is missing the {attribute} attribute')
            continue
        req = requests.head(pyproject_data['project']['data'][attribute])
        if not req.ok:
            natcap_requirement_errors.append(
                f'project.data.{attribute} could not be loaded')

    return None


def _valdiate_project_json_file(filepath):
    pass


def main(args=None):
    parser = argparse.ArgumentParser(
        "lint-metadata.py", description=())


if __name__ == '__main__':
    main()
