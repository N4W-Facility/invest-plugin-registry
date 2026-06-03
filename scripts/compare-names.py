import argparse
import difflib
import json
import os
import sys


def main(args=None):
    parser = argparse.ArgumentParser(os.path.basename(__file__))
    parser.add_argument("NEW_PLUGIN_JSON")
    parser.add_argument("MAIN_PLUGINS_JSON")
    parser.add_argument("TARGET_FILE")

    parsed_args = parser.parse_args(args)
    print(parsed_args)

    with open(parsed_args.NEW_PLUGIN_JSON, "r") as f:
        new_plugin_data = json.load(f)
    with open(parsed_args.MAIN_PLUGINS_JSON, "r") as f:
        main_plugins_data = json.load(f)

    new_name = new_plugin_data['plugin_name'].lower()
    existing_names = [plugin['plugin_name'].lower() for plugin in main_plugins_data]
    matches = difflib.get_close_matches(new_name, existing_names, cutoff=0.85)
    if matches:
        best_match = matches[0]
        score = difflib.SequenceMatcher(None, new_name, best_match).ratio()
        if score == 1.0:
            message = "❌ plugin has the same name as an existing plugin\n"
        else:
            message = (
                "ℹ️  plugin name was found to be similar to existing plugin name(s): "
                f"{matches}\n")
    else:
        message = "✅ plugin name is unique!\n"

    with open(parsed_args.TARGET_FILE, 'w') as target_file:
        target_file.write(message)


if __name__ == "__main__":
    main(sys.argv[1:])
