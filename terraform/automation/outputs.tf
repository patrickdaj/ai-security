output "report_bucket" {
  description = "S3 bucket where scan reports are written (one prefix per run)."
  value       = aws_s3_bucket.reports.bucket
}

output "codebuild_project" {
  description = "CodeBuild project that runs the pipeline."
  value       = aws_codebuild_project.scan.name
}

output "schedule_rule" {
  description = "EventBridge rule driving the schedule."
  value       = aws_cloudwatch_event_rule.schedule.name
}

output "triage_enabled" {
  description = "Whether AI triage runs (true when anthropic_secret_arn is set)."
  value       = local.triage_enabled
}
