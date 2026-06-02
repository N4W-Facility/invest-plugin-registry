# /// script
# requires-python = ">=3.6"
# dependencies = [
#     "requests",
# ]
# ///
import argparse
import functools
import hashlib
import json
import logging

import requests

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

RAW_REPO_PREFIX = (
    'https://raw.githubusercontent.com/natcap/invest-plugin-registry')


def _hashdict(source_dict):
    """Hash the contents of a dict for easier comparison."""
    encoded_data = json.dumps(source_dict).encode('utf-8')
    return hashlib.sha256(encoded_data, usedforsecurity=False).hexdigest()


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('pr_plugins_json', default='plugins.json')  # filepath to the local plugins json
    parser.add_argument('reference_plugins_json', default='main_plugins.json')
    parser.add_argument('target_json', default='new_content.json')

    parsed_args = parser.parse_args(args)

    with open(parsed_args.reference_plugins_json) as reference_json_file:
        reference_json = json.load(reference_json_file)
        LOGGER.debug(f"Reference json: {reference_json}")

    with open(parsed_args.pr_plugins_json) as pr_json_file:
        pr_json = json.load(pr_json_file)
        LOGGER.debug(f"PR json: {pr_json}")

    # Fail if no change to the pr json file.
    if pr_json == reference_json:
        parser.exit(1, "No changes found in the plugins json file.")

    # Fail if there isn't 1 more item in the pr json file than the reference.
    _serialize = functools.partial(json.dumps, sort_keys=True)
    pr_json_set = set(_serialize(d) for d in pr_json)
    reference_json_set = set(_serialize(d) for d in reference_json)

    # make sure that the only change is to the PR json
    if not (len(pr_json_set - reference_json_set) == 1 and
            len(reference_json_set - pr_json_set) == 0):
        parser.exit(
            2, ("Expected exactly 1 new object and that the reference JSON "
                "is unchanged"))

    # Compare individual entries to ensure all entries are unchanged
    source_data_hashed = {}
    for data_dict in reference_json:
        source_data_hashed[_hashdict(data_dict)] = data_dict

    nonmatching_data = []
    for data_dict in pr_json:
        data_hash = _hashdict(data_dict)
        if data_hash not in source_data_hashed:
            nonmatching_data.append(data_dict)

    if len(nonmatching_data) != 1:
        parser.exit(
            3, (
            "Some data in the json file has been modified relative to "
            f"{parsed_args._reference_git_ref}"))

    # We should now be confident that only the one object remains.
    # Extract it and return the git URL.
    # The entry (and all others) is linted in a different script.
    with open(parsed_args.target_json, 'w') as target_json_file:
        target_json_file.write(
            json.dumps(nonmatching_data[0], indent=4, sort_keys=True))


if __name__ == '__main__':
    main()
