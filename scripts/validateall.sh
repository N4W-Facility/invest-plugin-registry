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

# clone the new repo
REPO_URL=$(cat "$NEW_PLUGIN_DATA_FILE" | jq --raw-output .repo_url)
LOCAL_REPO_DIR=repo
if [ -e "$LOCAL_REPO_DIR" ]
then
    rm -rf "$LOCAL_REPO_DIR"
fi
git clone "$REPO_URL" "$LOCAL_REPO_DIR"

# Lint things
set +e
LINT_RESULTS_FILE=lint_results.txt
uv run --script scripts/lint-metadata.py \
  --target-file "$LINT_RESULTS_FILE" \
  "${LOCAL_REPO_DIR}/pyproject.toml" \
  "plugins.json"
ERRORS=$?

# Post results to the PR for review
write_comment "$LINT_RESULTS_FILE"

if [ "$ERRORS" != "0" ]
then
    echo "Failing the validation script because of validation errors."
    exit $ERRORS
fi


