<!-- Example output — illustrative deliverable of module 08, run against
     project/terraform (the misconfigured target). -->

# IaC Remediation — `project/terraform`

Checkov: 9 failed checks → remediations generated. 5 auto-apply (low risk), 4
held for review.

## AUTO-APPLY — S3 bucket missing encryption (CKV_AWS_19, low risk)
Satisfies: CIS-AWS-2.1.1
```diff
 resource "aws_s3_bucket" "public_assets" {
   bucket = "${var.name_prefix}-public-assets"
 }
+
+resource "aws_s3_bucket_server_side_encryption_configuration" "public_assets" {
+  bucket = aws_s3_bucket.public_assets.id
+  rule {
+    apply_server_side_encryption_by_default { sse_algorithm = "aws:kms" }
+  }
+}
```

## REVIEW — Over-permissioned CI role (CKV IAM, high risk)
Satisfies: CIS-AWS-1.16 · **held**: changing IAM may break deploys.
```diff
-      Action   = ["iam:CreatePolicyVersion", "iam:PassRole", "lambda:CreateFunction", "sts:AssumeRole"]
-      Resource = "*"
+      Action   = ["lambda:CreateFunction"]
+      Resource = "arn:aws:lambda:*:*:function:ci-*"
```

**Outcome:** 9 findings → review-ready diffs that clear on re-scan, with risky
IAM/network changes correctly gated for human sign-off.
