import argparse


def main(args=None):
    parser = argparse.ArgumentParser(__name__)
    parser.add_argument("LINTING_PY_SCRIPT")
    parser.add_argument("TARGET_PYODIDE_SCRIPT")

    parsed_args = parser.parse_args(args)

    with open(parsed_args.LINTING_PY_SCRIPT) as scriptfile:
        scriptdata = scriptfile.read()

    with open(parsed_args.TARGET_PYODIDE_SCRIPT) as pyodide_script:
        pyodide_data = pyodide_script.read()

    with open(parsed_args.TARGET_PYODIDE_SCRIPT, 'w') as pyodide_script:
        pyodide_script.write(
            pyodide_data.replace('{{__METADATA_LINTING_SCRIPT__}}', scriptdata))


if __name__ == '__main__':
    main()
