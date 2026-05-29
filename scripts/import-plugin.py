import argparse
import logging
import os
import sys
import tomllib

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


def main(args=None):
    parser = argparse.ArgumentParser(os.path.basename(__file__))
    parser.add_argument('PYPROJECT_TOML')
    parser.add_argument('TARGET_ERRORS')

    parsed_args = parser.parse_args(args)

    with open(parsed_args.PYPROJECT_TOML, 'rb') as pyproject_toml:
        tomldata = tomllib.load(pyproject_toml)

    project_name = tomldata['tool']['natcap']['invest']['package_name']

    sys.path.insert(
        0, os.path.join(os.path.dirname(parsed_args.PYPROJECT_TOML),
                        'src'))
    import_error = None
    try:
        LOGGER.info(
            f"Testing that module {project_name}.{project_name} imports")
        _ = __import__(f'{project_name}.{project_name}')
    except ImportError as e:
        import_error = str(e)

    with open(parsed_args.TARGET_ERRORS, 'w') as target_errors:
        if import_error is None:
            target_errors.write(
                f"✅ Plugin {project_name} imported successfully; imports are "
                "sufficient!\n")
        else:
            target_errors.write(
                f"❌ Plugin {project_name} did not import; error was: "
                f"{import_error}\n")


if __name__ == '__main__':
    main(sys.argv[1:])
