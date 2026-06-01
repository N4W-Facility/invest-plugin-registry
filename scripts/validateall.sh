#!/usr/bin/env sh
#
# Run through all validation scripts.
# Intended to be run through during github actions.
# For local development, messages that would be written to the PR by github
# actions are instead printed to the shell.
#
# Example call of this script, passing user, reponame, branch as parameters:
#
#   $ ./scripts/validateall.sh natcap invest-plugin-demo main

# The file to write output to.  If not provided, will write to stdout.
FILE="$1"
if [ -z "$FILE" ]; then
    FILE=/dev/stdout
else
    rm "$FILE"
fi

# Param 1 to the function is the file with contents to write out.
write_comment () {
    cat "$1" >> "$FILE"
}

# Be eXplicit about what's being run
set -x

# Fail on first error
set -e

# We are assuming that this script is running from the main repo and within a PR
curl -o plugins.json "https://raw.githubusercontent.com/natcap/invest-plugin-registry/main/plugins.json"
cat plugins.json  # for debugging

# Extract the new plugin information from plugins.json
NEW_PLUGIN_DATA_FILE=new_plugin.json
uv run --script scripts/extract-modified-json.py \
  plugins.json \
  main \
  "$NEW_PLUGIN_DATA_FILE"
cat "$NEW_PLUGIN_DATA_FILE"
VERSION="$(jq --raw-output .version $NEW_PLUGIN_DATA_FILE)"
echo "We will try to check out version $VERSION"

# clone the new repo
REPO_URL=$(cat "$NEW_PLUGIN_DATA_FILE" | jq --raw-output .repo_url)
LOCAL_REPO_DIR=repo
if [ -e "$LOCAL_REPO_DIR" ]
then
    rm -rf "$LOCAL_REPO_DIR"
fi
git clone "$REPO_URL" "$LOCAL_REPO_DIR"
cd "$LOCAL_REPO_DIR"
if ! git checkout "$VERSION"
then
    echo "❌ Version $VERSION from plugins.json not found as a tag in $REPO_URL" > errors.txt
    write_comment errors.txt
    exit 1
fi
cd ..

# Lint things
set +e  # disable failing on script errors
LINT_RESULTS_FILE=lint_results.txt
uv run --script scripts/lint-metadata.py \
  --target-file "$LINT_RESULTS_FILE" \
  "${LOCAL_REPO_DIR}/pyproject.toml" \
  "plugins.json"
ERRORS=$?

if [ "$ERRORS" != "0" ]
then
    echo "Failing the validation script because of validation errors."
    write_comment "$LINT_RESULTS_FILE"  # post comments for the PR
    exit $ERRORS
fi


# compare versions
VERSION_COMPARE="version_comparison.txt"
python scripts/compare-versions.py \
    "$LOCAL_REPO_DIR/pyproject.toml" \
    "$NEW_PLUGIN_DATA_FILE" \
    "$VERSION_COMPARE"

# now that linting has completed, extract plugin's information
PLUGIN_INFO="plugin_info.md"
python scripts/extract-plugin-info.py \
    "$LOCAL_REPO_DIR/pyproject.toml" \
    "$PLUGIN_INFO"

# Check that packages install and we can import all python files.
#
# miniconda is installed on github actions, so use that instead of mamba.
CONDA_ENV=envvalidate
ENV_FILENAME="environment.yml"
if [ -e "$CONDA_ENV" ]
then
    rm -rf "$CONDA_ENV"
fi
python scripts/build-env-yaml.py "$LOCAL_REPO_DIR/pyproject.toml" "$ENV_FILENAME"
conda env create -p "./$CONDA_ENV" --file="$ENV_FILENAME"

IMPORT_ERRORS="import-errors.txt"
"$CONDA_ENV/bin/python" scripts/import-plugin.py "$LOCAL_REPO_DIR/pyproject.toml" "$IMPORT_ERRORS"

FINAL_FILE="final.md"
cat "$LINT_RESULTS_FILE" "$VERSION_COMPARE" "$IMPORT_ERRORS" "$PLUGIN_INFO" > "$FINAL_FILE"
write_comment "$FINAL_FILE"
