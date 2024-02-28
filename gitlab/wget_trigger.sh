#!/bin/bash

# GitLab project ID
PROJECT_ID="YOUR_PROJECT_ID"
# Trigger token
TRIGGER_TOKEN="YOUR_TRIGGER_TOKEN"
# Reference to trigger (branch or tag)
REF_TO_TRIGGER="REF_TO_TRIGGER"
# GitLab instance URL, change if you're using GitLab Enterprise Edition
GITLAB_URL="https://gitlab.com"

# URL to call
URL="${GITLAB_URL}/api/v4/projects/${PROJECT_ID}/trigger/pipeline"

# POST data
POST_DATA="token=${TRIGGER_TOKEN}&ref=${REF_TO_TRIGGER}"

# Additional parameters can be added to the POST data if needed, for example:
# POST_DATA="${POST_DATA}&variables[MY_VARIABLE]=my_value"

wget --post-data "${POST_DATA}" --header="Content-Type: application/x-www-form-urlencoded" --no-check-certificate "${URL}" -O - 
