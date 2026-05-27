#!/usr/bin/env sh
#
# Run through all validation scripts.
# Intended to be run through during github actions.
# For local development, messages that would be written to the PR by github
# actions are instead printed to the shell.
#


# Expects $1 to be the filepath to the comment contents
write_comment () {
    # -z is true if the string has length 0.
    if [ -z "$GITHUB_ACTIONS" ];
    then
        set +x  # be nonexplicit
        echo "########### SIMULATED PR COMMENT ##############"
        cat "$1"
        echo ""
        echo "########### END SIMULATED PR COMMENT ##############"
        set -x  # reenable explicitness
    else
        # We're in github actions, so post to the relevant PR.
        gh pr comment "$PR_NUMBER" --body-file "$1"
    fi
}

# Be eXplicit about what's being run
set -x

# Fail on first error
set -e

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
    "$REPO_URL/pyproject.toml" \
    "$NEW_PLUGIN_DATA_FILE" \
    "$VERSION_COMPARE"

# now that linting has completed, extract plugin's information
PLUGIN_INFO="plugin_info.md"
python scripts/extract-plugin-info.py \
    "$REPO_URL/pyproject.toml" \
    "$PLUGIN_INFO"

FINAL_FILE="final.md"
cat "$LINT_RESULTS_FILE" "$VERSION_COMPARE" "$PLUGIN_INFO" >> "$FINAL_FILE"
write_comment "$FINAL_FILE"
