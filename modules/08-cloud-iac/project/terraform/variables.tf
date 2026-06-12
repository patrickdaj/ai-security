variable "region" {
  description = "AWS region (only used if you scan with a provider configured; not applied)."
  type        = string
  default     = "us-east-1"
}

variable "name_prefix" {
  description = "Prefix for resource names."
  type        = string
  default     = "vuln-lab"
}
