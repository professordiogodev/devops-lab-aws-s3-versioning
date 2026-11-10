#!/usr/bin/env bash
# The accident. Somebody overwrites the monthly report and deletes the customer list. Run with: ./incident.sh
set -u
ACCOUNT=$(aws sts get-caller-identity --query Account --output text 2>/dev/null) || { echo "No working AWS credentials." >&2; exit 1; }
B="clippy-reports-$ACCOUNT"
T=$(mktemp); printf 'GARBAGE GARBAGE GARBAGE\n' > "$T"
aws s3api put-object --bucket "$B" --key reports/2026-10.csv --body "$T" >/dev/null; rm -f "$T"
aws s3api delete-object --bucket "$B" --key customers.csv >/dev/null
echo "Somebody overwrote reports/2026-10.csv and deleted customers.csv in s3://$B. Can you get them back?"
