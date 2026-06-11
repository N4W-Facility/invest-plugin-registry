import argparse
import logging
import os
import sys
import tomllib

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

REQUIRED_ATTRS = ('execute', 'validate', 'MODEL_SPEC')


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
    missing_attributes = []
    try:
        LOGGER.info(
            f"Testing that module {project_name}.{project_name} imports")
        module = __import__(project_name)
        for attrname in REQUIRED_ATTRS:
            if not hasattr(module, attrname):
                missing_attributes.append(
                    f" Plugin module is missing the attribute {attrname}")
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

        if missing_attributes:
            for attr_msg in missing_attributes:
                target_errors.write(f"❌ {attr_msg}")
        else:
            target_errors.write(
                f"✅ Plugin {project_name} has all required attributes")


if __name__ == '__main__':
    main(sys.argv[1:])
