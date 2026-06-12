# DELIBERATELY MISCONFIGURED — a scan target, not deployable infrastructure.
#
# This module plants the misconfigurations modules 08 (Checkov/tfsec) and 11
# (CIEM attack paths) are meant to find. SCAN THE CODE, do not `terraform apply`
# it in a real account:
#
#   checkov -d .
#   tfsec .
#   trivy config .
#
# Each resource below maps to a finding the augmentation layer should triage and
# remediate (see module 08's remediation-as-code build).

terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# [public S3] no public-access block, public-read ACL, no encryption, no
# versioning. Checkov: CKV_AWS_18/19/20/21/53-56. Module 11 path 2's leaky bucket.
resource "aws_s3_bucket" "public_assets" {
  bucket = "${var.name_prefix}-public-assets"
}

resource "aws_s3_bucket_public_access_block" "public_assets" {
  bucket                  = aws_s3_bucket.public_assets.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "public_read" {
  bucket = aws_s3_bucket.public_assets.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid       = "PublicRead"
      Effect    = "Allow"
      Principal = "*"
      Action    = "s3:GetObject"
      Resource  = "${aws_s3_bucket.public_assets.arn}/*"
    }]
  })
}

# [open ingress] SSH from anywhere. tfsec: aws-ec2-no-public-ingress-sgr.
resource "aws_security_group" "open_ssh" {
  name        = "${var.name_prefix}-open-ssh"
  description = "Intentionally over-exposed"

  ingress {
    description = "SSH from the entire internet"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# [over-permissioned role] the CIEM module-11 "ci-deploy -> admin" path: a CI
# role that can rewrite its own policy, pass roles, and assume anything.
resource "aws_iam_role" "ci_deploy" {
  name = "${var.name_prefix}-ci-deploy"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "ci_deploy_privesc" {
  name = "ci-deploy-privesc"
  role = aws_iam_role.ci_deploy.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "iam:CreatePolicyVersion",
        "iam:PassRole",
        "lambda:CreateFunction",
        "sts:AssumeRole",
      ]
      Resource = "*" # wildcard on privilege-escalation actions
    }]
  })
}
