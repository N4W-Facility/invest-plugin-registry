import argparse
import os
import sys
import tomllib

YML_FILE = """\
name: envvalidate
channels:
- conda-forge
- defaults
dependencies:
- pip
{condadeps}
- pip:
{pipdeps}
"""

def main(args=None):
    parser = argparse.ArgumentParser(os.path.basename(__file__))
    parser.add_argument('PYPROJECT_TOML')
    parser.add_argument('TARGET_YML')

    parsed_args = parser.parse_args(args)

    with open(parsed_args.PYPROJECT_TOML, 'rb') as pyproject_toml:
        tomldata = tomllib.load(pyproject_toml)

    condadeps = '\n'.join([f'- {name}' for name in
            tomldata['tool']['natcap']['invest']['conda_dependencies']])
    pipdeps = '\n'.join(
        [f'  - {name}' for name in tomldata['project']['dependencies']])
    with open(parsed_args.TARGET_YML, 'w') as target_yml:
        target_yml.write(
            YML_FILE.format(
                condadeps=condadeps,
                pipdeps=pipdeps))


if __name__ == '__main__':
    main(sys.argv[1:])
