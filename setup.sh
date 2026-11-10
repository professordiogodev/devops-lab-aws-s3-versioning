#!/usr/bin/env bash
# Creates the reports bucket with two files (./setup.sh), or puts the two original files back (./setup.sh --reupload).
set -u
ACCOUNT=$(aws sts get-caller-identity --query Account --output text 2>/dev/null) || { echo "No working AWS credentials (aws sts get-caller-identity fails)." >&2; exit 1; }
B="clippy-reports-$ACCOUNT"
put() { local k="$1" body="$2" t; t=$(mktemp); printf '%b' "$body" > "$t"; aws s3api put-object --bucket "$B" --key "$k" --body "$t" >/dev/null; rm -f "$t"; }
if [ "${1:-}" != "--reupload" ]; then
  if aws s3api head-bucket --bucket "$B" >/dev/null 2>&1; then echo "Bucket $B already exists. Use ./setup.sh --reupload to put the original files back."; exit 0; fi
  aws s3api create-bucket --bucket "$B" --region us-east-1 >/dev/null || exit 1
  aws s3api put-bucket-tagging --bucket "$B" --tagging 'TagSet=[{Key=lab,Value=aws-s3-versioning}]'
fi
put reports/2026-10.csv 'month,links_created\n2026-10,1200\n'
put customers.csv 'id,plan\n1,pro\n2,free\n'
echo "s3://$B now holds the two original files: reports/2026-10.csv and customers.csv"
