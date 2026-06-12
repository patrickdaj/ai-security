# Automation

The toolchain runs unattended via the headless [`automation/`](https://github.com/patrickdaj/ai-security/tree/main/automation)
pipeline, CI workflows, and Terraform. You build this yourself in
[Module 16](modules/16-automation-pipelines.md); the pieces below are the
reference.

## Scheduled scan pipeline (Terraform)

{%
   include-markdown "../terraform/automation/README.md"
%}

## Misconfigured scan target (Terraform)

{%
   include-markdown "../modules/08-cloud-iac/project/terraform/README.md"
%}
