import argparse
import json
import os
import sys
import tomllib


def main(args=None):
    parser = argparse.ArgumentParser(os.path.basename(__file__))
    parser.add_argument("PYPROJECT_PATH")
    parser.add_argument("PLUGIN_DATA_JSON")
    parser.add_argument("TARGET_FILE")

    parsed_args = parser.parse_args(args)
    print(parsed_args)

    with open(parsed_args.PYPROJECT_PATH, "rb") as f:
        pyproject = tomllib.load(f)
    with open(parsed_args.PLUGIN_DATA_JSON, "r") as f:
        plugin_data = json.load(f)

    with open(parsed_args.TARGET_FILE, 'w') as target_file:
        try:
            if pyproject['project']['version'] != plugin_data['version']:
                target_file.write(
                    "❌ plugins.json and pyproject.toml have different "
                    "versions\n")
                parser.exit(1, "Failing because of detected version mismatch")
            else:
                target_file.write(
                    "✅ plugins.json and pyproject.toml have matching "
                    "version\n")
        except KeyError:
            target_file.write(
                "ℹ️  Could not check versions; might be dynamic\n")


if __name__ == "__main__":
    main(sys.argv[1:])
