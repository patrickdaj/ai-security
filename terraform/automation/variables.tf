variable "region" {
  description = "AWS region to deploy the scheduled scanner into."
  type        = string
  default     = "us-east-1"
}

variable "name" {
  description = "Name prefix for created resources."
  type        = string
  default     = "ai-sec-pipeline"
}

variable "repo_url" {
  description = "Git URL of the repository CodeBuild scans (this curriculum, or your target)."
  type        = string
}

variable "repo_branch" {
  description = "Branch to check out."
  type        = string
  default     = "main"
}

variable "scan_target" {
  description = "Path within the checked-out repo to scan."
  type        = string
  default     = "."
}

variable "fail_on" {
  description = "Severity at/above which the pipeline reports failure (info|low|medium|high|critical)."
  type        = string
  default     = "high"
}

variable "schedule_expression" {
  description = "EventBridge schedule for the scan (cron or rate)."
  type        = string
  default     = "cron(0 6 * * ? *)" # daily at 06:00 UTC
}

variable "anthropic_secret_arn" {
  description = "Secrets Manager ARN holding the ANTHROPIC_API_KEY. Empty string = run --no-triage (aggregation only)."
  type        = string
  default     = ""
}

variable "tags" {
  description = "Tags applied to all resources."
  type        = map(string)
  default     = { project = "ai-security-curriculum", managed_by = "terraform" }
}
