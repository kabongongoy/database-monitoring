# variable "db_identifier" {}
# variable "is_cluster" { default = false }
# variable "environment" {}
# variable "cpu_threshold" { default = 80 }
# variable "memory_threshold" { default = 1000000000 }
# variable "slack_webhook_url" { sensitive = true }
# variable "slack_channel" { default = "#database-alerts" }
# variable "tags" { type = map(string) }

# variable "db_identifiers" {
#   description = "List of database identifiers to monitor"
#   type        = list(string)
# }

# (Keep all other existing variables)


# Database Configuration
variable "db_identifiers" {
  description = "List of database identifiers to monitor (e.g., ['db-prod-1', 'db-prod-2'])"
  type        = list(string)
}

variable "is_cluster" {
  description = "Set to true for Aurora clusters, false for RDS instances"
  type        = bool
  default     = false
}

# Alert Thresholds
variable "cpu_threshold" {
  description = "CPU utilization percentage threshold (e.g., 85 for 85%)"
  type        = number
}

variable "memory_threshold" {
  description = "Freeable memory threshold in bytes (e.g., 2000000000 for 2GB)"
  type        = number
}

variable "latency_threshold" {
  description = "Latency threshold in seconds (e.g., 0.5)"
  type        = number
}

# Slack Configuration
variable "slack_webhook_url" {
  description = "Slack incoming webhook URL (set via TF_VAR_slack_webhook_url)"
  type        = string
  sensitive   = true
}

variable "slack_channel" {
  description = "Slack channel for alerts (e.g., '#database-alerts')"
  type        = string
}

# Naming/Tagging
variable "alarm_name_prefix" {
  description = "Prefix for alarm names (e.g., 'prod-db')"
  type        = string
  default     = "db-alarm"
}

variable "environment" {
  description = "Environment name (e.g., 'production', 'staging')"
  type        = string
}

variable "tags" {
  description = "Additional tags for all resources"
  type        = map(string)
  default     = {}
}


variable "free_storage_threshold" {
  type        = number
  default     = 10368709120  # 5 GB in bytes
  description = "Threshold for free storage in bytes"
}
