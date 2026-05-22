# /// script
# requires-python = ">=3.6"
# dependencies = [
#     "requests",
# ]
# ///
import argparse
import hashlib
import json

import requests

RAW_REPO_PREFIX = (
    'https://raw.githubusercontent.com/natcap/invest-plugin-registry')


def _hashdict(source_dict):
    """Hash the contents of a dict for easier comparison."""
    encoded_data = json.dumps(source_dict).encode('utf-8')
    return hashlib.sha256(encoded_data, usedforsecurity=False).hexdigest()


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('plugins_json', default='plugins.json')  # filepath to the local plugins json
    parser.add_argument('reference_git_ref', default='main')  # The head ref, e.g. main, of the reference file
    parser.add_argument('target_json', default='new_content.json')

    parsed_args = parser.parse_args(args)

    reference_url = (
        f'{RAW_REPO_PREFIX}/refs/heads/{parsed_args.reference_git_ref}'
        '/plugins.json')
    resp = requests.get(reference_url)
    resp.raise_for_status()  # shouldn't error but you never know
    reference_json = resp.json()

    with open(parsed_args.plugins_json) as pr_json_file:
        pr_json = json.load(pr_json_file)

    # Fail if no change to the pr json file.
    if pr_json == reference_json:
        parser.error("No changes found in the plugins json file.")

    # Fail if there isn't 1 more item in the pr json file than the reference.
    n_changed_objects = len(pr_json) - len(reference_json)
    if n_changed_objects != 1:
        parser.error(
            f"Expected exactly 1 new object, not {n_changed_objects}")

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
        parser.error(
            "Some data in the json file has been modified relative to "
            f"{parsed_args._reference_git_ref}")

    # We should now be confident that only the one object remains.
    # Extract it and return the git URL.
    # The entry (and all others) is linted in a different script.
    with open(parsed_args.target_json, 'w') as target_json_file:
        target_json_file.write(
            json.dumps(nonmatching_data[0], indent=4, sort_keys=True))


if __name__ == '__main__':
    main()
