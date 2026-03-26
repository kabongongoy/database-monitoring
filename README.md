# database-monitoring

Terraform module that provisions AWS CloudWatch alarms for RDS and Aurora databases and delivers formatted alerts to a Slack channel via SNS and Lambda.

## Architecture

```
CloudWatch Alarms → SNS Topic → Lambda (Python) → Slack
```

- **CloudWatch** monitors RDS/Aurora metrics and triggers alarms on threshold breaches
- **SNS** receives alarm state changes and fans out to the Lambda function
- **Lambda** (`slack_notifier.py`) formats the alert and posts it to Slack with metric-specific emojis, colour coding, and Australian local time

## Monitored Metrics

| Metric | Alarm condition |
|---|---|
| CPU Utilisation | Above threshold % for 5 minutes |
| Freeable Memory | Below threshold bytes for 5 minutes |
| Free Storage Space | Below threshold bytes for 5 minutes |
| Database Connections | Above threshold for 5 minutes |
| Deadlocks | Any deadlock detected in 5 minutes |

## Prerequisites

- Terraform >= 1.0
- AWS provider ~> 5.0
- AWS credentials configured
- A Slack incoming webhook URL

## Usage

```hcl
module "db_monitoring" {
  source = "./modules/db-monitoring"

  # One or more RDS instance or Aurora cluster identifiers
  db_identifiers = ["prod-db-1", "prod-db-2"]
  is_cluster     = false   # true for Aurora clusters

  # Alert thresholds
  cpu_threshold          = 85          # percent
  memory_threshold       = 2000000000  # bytes (2 GB)
  latency_threshold      = 100         # connections
  free_storage_threshold = 5368709120  # bytes (5 GB)

  # Slack
  slack_webhook_url = var.slack_webhook_url
  slack_channel     = "#database-alerts"

  # Naming
  alarm_name_prefix = "prod-db"
  environment       = "production"

  tags = {
    Team    = "Platform"
    Project = "database-monitoring"
  }
}
```

## Inputs

### Root module

| Name | Description | Type | Default | Required |
|---|---|---|---|---|
| `db_identifiers` | List of RDS instance or Aurora cluster identifiers | `list(string)` | — | yes |
| `is_cluster` | Set `true` for Aurora clusters, `false` for RDS instances | `bool` | `false` | no |
| `cpu_threshold` | CPU utilisation threshold (%) | `number` | — | yes |
| `memory_threshold` | Freeable memory threshold (bytes) | `number` | — | yes |
| `latency_threshold` | Connection count threshold | `number` | — | yes |
| `free_storage_threshold` | Free storage threshold (bytes) | `number` | `10368709120` | no |
| `slack_webhook_url` | Slack incoming webhook URL | `string` | — | yes |
| `slack_channel` | Slack channel for alerts (e.g. `#database-alerts`) | `string` | — | yes |
| `alarm_name_prefix` | Prefix applied to all alarm names | `string` | `"db-alarm"` | no |
| `environment` | Environment name (`production`, `staging`, etc.) | `string` | — | yes |
| `tags` | Tags applied to all resources | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|---|---|
| `alarm_sns_topic_arn` | ARN of the SNS topic receiving alarm notifications |
| `lambda_function_arn` | ARN of the Slack notifier Lambda function |

## Resources Created

| Resource | Purpose |
|---|---|
| `aws_cloudwatch_metric_alarm` | One alarm per metric per database identifier |
| `aws_sns_topic` | Receives CloudWatch alarm state changes |
| `aws_sns_topic_subscription` | Connects SNS topic to the Lambda function |
| `aws_lambda_function` | Formats and forwards alerts to Slack |
| `aws_iam_role` | Lambda execution role |
| `aws_iam_role_policy_attachment` | Attaches basic Lambda execution policy (CloudWatch Logs) |
| `aws_lambda_permission` | Allows SNS to invoke the Lambda function |
| `aws_sns_topic_policy` | Allows CloudWatch to publish to the SNS topic |

## Deployment

```bash
# 1. Initialise Terraform
terraform init

# 2. Set sensitive variable (never commit this)
export TF_VAR_slack_webhook_url="https://hooks.slack.com/services/..."

# 3. Review the plan
terraform plan

# 4. Apply
terraform apply
```

## Slack Notifications

Alerts are posted with metric-specific formatting:

| Metric | Emoji | Colour |
|---|---|---|
| CPU Utilisation | 🖥️ | Red-orange |
| Freeable Memory | 🧠 | Orange |
| Free Storage | 💾 | Red |
| Connections/Latency | 🐢 | Purple |
| Deadlocks | 🔒 | Pink |

Each notification includes the current value, configured threshold, database identifier, environment, and the local Australian time (AEST/AEDT with automatic DST handling).

## Module Structure

```
.
├── main.tf                          # Root module — calls db-monitoring module
├── variables.tf                     # Root input variables
├── outputs.tf                       # Root outputs
├── providers.tf                     # AWS provider configuration
└── modules/
    └── db-monitoring/
        ├── main.tf                  # CloudWatch alarms and SNS resources
        ├── lambda.tf                # Lambda function and archive packaging
        ├── iam.tf                   # IAM role, policies, and permissions
        ├── variables.tf             # Module input variables
        ├── outputs.tf               # Module outputs
        └── lambda/
            └── slack_notifier.py    # Python Lambda handler
```

## Security Notes

- `slack_webhook_url` is marked `sensitive = true` — it will not appear in Terraform plan output or state diffs
- Pass it via the `TF_VAR_slack_webhook_url` environment variable rather than storing it in `.tfvars` files
- The Lambda execution role uses the minimal `AWSLambdaBasicExecutionRole` managed policy (CloudWatch Logs only)
