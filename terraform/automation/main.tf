# Scheduled security-scan pipeline on AWS: EventBridge fires CodeBuild on a
# cron; CodeBuild clones the repo, runs `python -m automation`, and writes the
# report to an encrypted S3 bucket. Least-privilege IAM throughout.
#
# Review before applying — this provisions real, billable resources. Apply in a
# sandbox account.

data "aws_caller_identity" "current" {}

locals {
  triage_enabled = var.anthropic_secret_arn != ""
}

# --- Report bucket (done right — contrast with the module-08 scan target) ----

resource "aws_s3_bucket" "reports" {
  bucket = "${var.name}-reports-${data.aws_caller_identity.current.account_id}"
  tags   = var.tags
}

resource "aws_s3_bucket_public_access_block" "reports" {
  bucket                  = aws_s3_bucket.reports.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "reports" {
  bucket = aws_s3_bucket.reports.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
    }
  }
}

resource "aws_s3_bucket_versioning" "reports" {
  bucket = aws_s3_bucket.reports.id
  versioning_configuration {
    status = "Enabled"
  }
}

# --- CodeBuild project --------------------------------------------------------

resource "aws_cloudwatch_log_group" "build" {
  name              = "/codebuild/${var.name}"
  retention_in_days = 30
  tags              = var.tags
}

resource "aws_iam_role" "build" {
  name = "${var.name}-build"
  tags = var.tags
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "codebuild.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "build" {
  name = "${var.name}-build"
  role = aws_iam_role.build.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = concat([
      {
        Sid      = "Logs"
        Effect   = "Allow"
        Action   = ["logs:CreateLogStream", "logs:PutLogEvents"]
        Resource = "${aws_cloudwatch_log_group.build.arn}:*"
      },
      {
        Sid      = "WriteReports"
        Effect   = "Allow"
        Action   = ["s3:PutObject"]
        Resource = "${aws_s3_bucket.reports.arn}/*"
      }
      ], local.triage_enabled ? [{
        Sid      = "ReadApiKey"
        Effect   = "Allow"
        Action   = ["secretsmanager:GetSecretValue"]
        Resource = var.anthropic_secret_arn
    }] : [])
  })
}

resource "aws_codebuild_project" "scan" {
  name         = var.name
  description  = "Scheduled security scan + AI triage pipeline."
  service_role = aws_iam_role.build.arn
  tags         = var.tags

  artifacts {
    type = "NO_ARTIFACTS"
  }

  environment {
    compute_type    = "BUILD_GENERAL1_SMALL"
    image           = "aws/codebuild/standard:7.0"
    type            = "LINUX_CONTAINER"
    privileged_mode = false

    environment_variable {
      name  = "REPORT_BUCKET"
      value = aws_s3_bucket.reports.bucket
    }
    environment_variable {
      name  = "SCAN_TARGET"
      value = var.scan_target
    }
    environment_variable {
      name  = "FAIL_ON"
      value = var.fail_on
    }
    environment_variable {
      name  = "TRIAGE_ENABLED"
      value = tostring(local.triage_enabled)
    }

    dynamic "environment_variable" {
      for_each = local.triage_enabled ? [1] : []
      content {
        name  = "ANTHROPIC_API_KEY"
        value = var.anthropic_secret_arn
        type  = "SECRETS_MANAGER"
      }
    }
  }

  logs_config {
    cloudwatch_logs {
      group_name = aws_cloudwatch_log_group.build.name
    }
  }

  source {
    type      = "GITHUB"
    location  = var.repo_url
    buildspec = <<-YAML
      version: 0.2
      phases:
        install:
          runtime-versions:
            python: 3.12
          commands:
            - pip install -e . && pip install semgrep
            - curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin
            - curl -sfL https://raw.githubusercontent.com/gitleaks/gitleaks/master/scripts/install.sh | sh -s -- -b /usr/local/bin || true
        build:
          commands:
            - |
              if [ "$TRIAGE_ENABLED" = "true" ]; then
                python -m automation --target "$SCAN_TARGET" --out report --fail-on "$FAIL_ON" -v
              else
                python -m automation --target "$SCAN_TARGET" --out report --fail-on "$FAIL_ON" --no-triage -v
              fi
              echo "PIPELINE_EXIT=$?" > pipeline.exit
        post_build:
          commands:
            - aws s3 cp report/ "s3://$REPORT_BUCKET/$(date +%Y-%m-%d-%H%M)/" --recursive
            - . ./pipeline.exit; exit "$${PIPELINE_EXIT:-0}"
    YAML
  }

  source_version = var.repo_branch
}

# --- EventBridge schedule -----------------------------------------------------

resource "aws_iam_role" "events" {
  name = "${var.name}-events"
  tags = var.tags
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "events.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "events" {
  name = "${var.name}-events"
  role = aws_iam_role.events.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["codebuild:StartBuild"]
      Resource = aws_codebuild_project.scan.arn
    }]
  })
}

resource "aws_cloudwatch_event_rule" "schedule" {
  name                = "${var.name}-schedule"
  description         = "Triggers the security-scan pipeline."
  schedule_expression = var.schedule_expression
  tags                = var.tags
}

resource "aws_cloudwatch_event_target" "codebuild" {
  rule     = aws_cloudwatch_event_rule.schedule.name
  arn      = aws_codebuild_project.scan.arn
  role_arn = aws_iam_role.events.arn
}
