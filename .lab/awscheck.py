#!/usr/bin/env python3
import json, os, subprocess, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(ROOT)
ACCOUNT = sys.argv[1]
B = "clippy-reports-" + ACCOUNT
passed = failed = 0


def check(desc, ok, hint=""):
    global passed, failed
    if ok:
        passed += 1; print("PASS  " + desc)
    else:
        failed += 1; print("FAIL  " + desc + (("   -> " + hint) if hint else ""))


def aws(*a):
    try:
        return json.loads(subprocess.check_output(("aws",) + a + ("--output", "json"), stderr=subprocess.DEVNULL, timeout=60) or "null")
    except Exception:
        return None


def body(key):
    r = subprocess.run(["aws", "s3", "cp", "s3://%s/%s" % (B, key), "-"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


check("no AWS keys in the repository", subprocess.run("git grep -lE 'AKIA[0-9A-Z]{16}' -- . ':!.lab' ':!verify.sh'", shell=True, capture_output=True, text=True).stdout.strip() == "")
print("== The bucket ==")
check("the bucket %s exists" % B, subprocess.run("aws s3api head-bucket --bucket %s" % B, shell=True, capture_output=True).returncode == 0, "./setup.sh")
check("versioning is Enabled", (aws("s3api", "get-bucket-versioning", "--bucket", B) or {}).get("Status") == "Enabled")
c = (aws("s3api", "get-public-access-block", "--bucket", B) or {}).get("PublicAccessBlockConfiguration", {})
check("all four public access block options are on", len(c) == 4 and all(c.values()))
enc = ((aws("s3api", "get-bucket-encryption", "--bucket", B) or {}).get("ServerSideEncryptionConfiguration", {}).get("Rules") or [{}])[0]
check("default encryption is on", enc.get("ApplyServerSideEncryptionByDefault", {}).get("SSEAlgorithm") in ("AES256", "aws:kms"))
lc = (aws("s3api", "get-bucket-lifecycle-configuration", "--bucket", B) or {}).get("Rules", [])
nc = any(r.get("Status") == "Enabled" and 30 <= r.get("NoncurrentVersionExpiration", {}).get("NoncurrentDays", 0) <= 365 for r in lc)
mp = any(r.get("Status") == "Enabled" and 0 < r.get("AbortIncompleteMultipartUpload", {}).get("DaysAfterInitiation", 0) <= 7 for r in lc)
check("lifecycle: old (noncurrent) versions expire after 30 to 365 days", nc)
check("lifecycle: incomplete multipart uploads are aborted within 7 days", mp)
tags = {t["Key"]: t["Value"] for t in (aws("s3api", "get-bucket-tagging", "--bucket", B) or {}).get("TagSet", [])}
check("the bucket is tagged lab=aws-s3-versioning", tags.get("lab") == "aws-s3-versioning")

print("== The recovery ==")
check("reports/2026-10.csv holds the ORIGINAL report again", body("reports/2026-10.csv") == "month,links_created\n2026-10,1200\n", "restore the good version")
check("customers.csv exists again with the original content", body("customers.csv") == "id,plan\n1,pro\n2,free\n", "remove the delete marker or copy the old version back")
vs = [v for v in (aws("s3api", "list-object-versions", "--bucket", B, "--prefix", "reports/2026-10.csv") or {}).get("Versions", []) if v["Key"] == "reports/2026-10.csv"]
check("the report has at least 3 versions (original, garbage, restored), so you recovered with versioning ON", len(vs) >= 3, "found %d" % len(vs))
check("the garbage version is still in the history (you did not erase the evidence)", any(v["Size"] == 24 for v in vs))
print()
print(("ALL CHECKS PASSED (%d/%d)" % (passed, passed)) if failed == 0 else ("%d check(s) failed, %d passed" % (failed, passed)))
sys.exit(1 if failed else 0)
