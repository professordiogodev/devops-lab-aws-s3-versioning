#!/usr/bin/env bash
# Empties the bucket (every version and delete marker) and deletes it. Run with: ./teardown.sh
set -u
ACCOUNT=$(aws sts get-caller-identity --query Account --output text 2>/dev/null) || { echo "No working AWS credentials." >&2; exit 1; }
B="clippy-reports-$ACCOUNT"
if aws s3api head-bucket --bucket "$B" >/dev/null 2>&1; then
  python3 - "$B" <<'PY'
import json, subprocess, sys
b = sys.argv[1]
while True:
    out = subprocess.check_output(["aws", "s3api", "list-object-versions", "--bucket", b, "--max-items", "500", "--output", "json"])
    v = json.loads(out or "{}")
    objs = [{"Key": x["Key"], "VersionId": x["VersionId"]} for x in (v.get("Versions") or []) + (v.get("DeleteMarkers") or [])]
    if not objs:
        break
    subprocess.check_call(["aws", "s3api", "delete-objects", "--bucket", b, "--delete", json.dumps({"Objects": objs, "Quiet": True})], stdout=subprocess.DEVNULL)
    print("  deleted", len(objs), "versions")
PY
  aws s3api delete-bucket --bucket "$B" && echo "deleted s3://$B"
fi
echo "Now run ./verify-teardown.sh"
