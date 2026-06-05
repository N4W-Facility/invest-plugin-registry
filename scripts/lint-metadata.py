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
import collections
import json
import logging
import os
import re
import sys
import tomllib
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.parse import urlsplit

if 'pyodide' in sys.modules:
    from pyodide.http.pyxhr import get
    from pyodide.http.pyxhr import head
else:
    from requests import get
    from requests import head

import validate_pyproject.api  # requires packaging>=24.2 for enforcement.

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

ALLOWED_PLUGIN_TYPES = [
    'preprocessing', 'postprocessing', 'workflow', 'invest_model_variant',
    'new_model', 'other']

Required = collections.namedtuple('Required', ['tomlattr'])
Optional = collections.namedtuple('Optional', ['tomlattr'])

def _get_pyproject_attr(tomldata, attr):
    subtomldata = tomldata
    for subattr in attr.split('.'):
        if subattr not in subtomldata:
            # Raise an error to distinguish from returning the value itself.
            raise ValueError(
                f"Pyproject.toml attribute not found: {attr}")
        else:
            subtomldata = subtomldata[subattr]

    # by the time we get to this point, it's just the attribute value.
    return subtomldata


def _write_pyproject_attr(tomldata, attr, new_value):
    subtomldata = tomldata
    keys_list = attr.split('.')
    max_depth = len(keys_list) - 1
    for depth, subattr in enumerate(keys_list):
        if subattr not in subtomldata and depth == max_depth:
            subtomldata[subattr] = new_value
        else:
            subtomldata = subtomldata[subattr]


def _test_url(url):
    if 'pyodide' in sys.modules:
        # ℹ️  Cannot test URL in pyodide environment due to CORS restrictions
        return None
    else:
        req = head(url)
        if not req.ok:
            return f"Could not load URL {url}"


def _is_nonempty(s):
    if len(s) == 0:
        return "Expected text, but didn't find anything"


def _file_exists(filepath):
    if filepath.startswith('https://'):
        resp = head(filepath)
        if not resp.ok:
            return f"Could not find file at {filepath}"
    if not os.path.exists(filepath):
        return f"Could not find local file {filepath}"


def _load_pyproject_toml(filepath_or_url):
    """Load a pyproject.toml file.

    If there are any linked files, those are loaded too.

    Args:
        filepath_or_url (str): The local filepath or URL to a
            pyproject.toml file.

    Returns:
        tomldata (dict): The loaded dictionary with toml data.
    """
    is_url = filepath_or_url.startswith('https://')

    if is_url:
        parsed_url = urlparse(filepath_or_url)
        is_gitlab = (
            '/api/v4/projects/'in filepath_or_url and
            parsed_url.netloc != 'github.com')

        req = get(filepath_or_url)
        try:
            pyproject_data = tomllib.loads(req.text)
        except tomllib.TOMLDecodeError as e:
            print(f"Could not parse file: {str(e)} at {filepath_or_url}")
            print(req.text)
            raise e
        pyproject_dir = os.path.dirname(urlsplit(filepath_or_url).path)
    else:
        pyproject_dir = os.path.dirname(filepath_or_url)
        with open(filepath_or_url, 'rb') as tomlfile:
            pyproject_data = tomllib.load(tomlfile)

    # Any other attributes that we expect to be files, just include them here
    # in this list.
    for attrname in [
            'project.readme',
            'project.license-files',
            'tool.natcap.invest.registry_description',
            ]:
        try:
            filenames = _get_pyproject_attr(pyproject_data, attrname)
            if not isinstance(filenames, list):
                filenames = [filenames]

            for filename in filenames:
                if is_url:
                    if is_gitlab:
                        # There are parameters to worry about, so handle those
                        # with a simplistic find/replace
                        new_url = filepath_or_url.replace(
                            'files/pyproject.toml/raw',
                            f'files/{filename}/raw')
                    else:
                        # It's github, we can just urljoin the new file to the
                        # url.
                        new_url = urljoin(filepath_or_url, filename)
                    resp = get(new_url)
                    _write_pyproject_attr(
                        pyproject_data, attrname, resp.text)
                else:
                    filename = os.path.join(pyproject_dir, filename)
                    if os.path.exists(filename):
                        with open(filename) as opened_file:
                            _write_pyproject_attr(
                                pyproject_data, attrname, opened_file.read())
        except ValueError:
            continue
    return pyproject_data


def _validate_pyproject_file(filepath):
    validator = validate_pyproject.api.Validator()

    pyproject_data = _load_pyproject_toml(filepath)

    # Check for the standard pyproject.toml validation requirements
    try:
        validator(pyproject_data)
    except validate_pyproject.errors.ValidationError as error:
        # error.summary is the 1-line error message
        # error.details is the full, multi-hundred-line description
        # error.message has both error.summary, error.details.
        return f"❌ Could not load pyproject.toml: {error.summary}"

    natcap_requirement_errors = []
    attrs_to_validate = {
        Required('project.urls.Documentation'): _test_url,
        Required('project.urls.Issues'): _test_url,
        Required('project.urls.Repository'): _test_url,
        Required('project.name'): _is_nonempty,
        Required('project.description'): _is_nonempty,
        Required('project.readme'): _is_nonempty,
        Required('project.license'): _is_nonempty,
        Required('project.license-files'): _is_nonempty,
        Optional('tool.natcap.invest.registry_description'): _is_nonempty,
    }
    for attr, test_callable in attrs_to_validate.items():
        is_required = isinstance(attr, Required)
        attrname = attr.tomlattr
        try:
            value = _get_pyproject_attr(pyproject_data, attrname)
        except ValueError:
            if is_required:
                natcap_requirement_errors.append(
                    'Pyproject.toml is missing the required attribute '
                    f'{attrname}')
            else:
                LOGGER.debug(f"Attribute {attrname} is optional and not "
                             "provided; skipping")
            continue

        test_result = test_callable(value)
        if test_result is not None:
            natcap_requirement_errors.append(
                f'Pyproject.toml {attr}: {test_result}')

    # Add any unique tests here
    # Required('project.authors/maintainers'): ,
    # Either or both project.authors, project.maintainers must be defined
    # The details are validated by validate_pyproject
    one_found = False
    for attr in ['project.authors', 'project.maintainers']:
        try:
            _ = _get_pyproject_attr(pyproject_data, attr)
            one_found = True
        except ValueError:
            pass

    if not one_found:
        natcap_requirement_errors.append(
            "Either project.authors or project.maintainers (or both) must be "
            "defined in your pyproject.toml file")

    if natcap_requirement_errors:
        return (
            f"{filepath} was found to have validation errors:\n"
            + "\n".join(f"❌ {issue}" for issue in natcap_requirement_errors))

    return None


def _validate_project_json_file(filepath):
    try:
        with open(filepath, 'r') as project_json:
            json_data = json.load(project_json)
    except json.decoder.JSONDecodeError as error:
        return f"❌ Could not parse JSON file at {filepath}: {str(error)}"

    # We're assuming that the top-level object is an array
    issues = []
    for object_num, plugin_data in enumerate(json_data):
        if "repo_url" in plugin_data:
            url = plugin_data['repo_url']
            req = head(url)
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
            + "\n".join(f"❌ {issue}" for issue in issues))
    return None


def main(args=None):
    LOGGER.debug(args)
    parser = argparse.ArgumentParser(
        "lint-metadata.py", description=(
            "A script for linting metadata in pyproject.toml and plugins.json."
        ))
    parser.add_argument('PYPROJECT_TOML_FILE', help="path to a pyproject.toml file")
    parser.add_argument('PLUGIN_JSON_FILE',
                        help="path to the plugin.json file")
    parser.add_argument(
        '--target-file',
        default='',
        help=("Where output should be written. If not provided, output is "
              "written to stdout"))

    parsed_args = parser.parse_args(args)

    # Restart the file so we can append to it later.
    if parsed_args.target_file:
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
        _write_to_file("✅ No errors found in the project!\n")
    else:
        error_vars = []
        for filename, var in [('pyproject.toml', pyproject_errors),
                              ('plugins.json', json_errors)]:
            if var is None:
                _write_to_file(
                    f"\n✅ No validation errors found in {filename}\n")
            else:
                error_vars.append(var)
        errors = '\n'.join(error_vars)
        parser.exit(1, f"Linting errors found: {errors}")


if __name__ == '__main__':
    # If pyodide is running in sys.modules, ignore the main() function since we
    # want to import and run specific functions from this script.
    if 'pyodide' not in sys.modules:
        main(sys.argv[1:])
