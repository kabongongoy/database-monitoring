variable "db_identifiers" {
  description = "List of RDS/Aurora database identifiers to monitor"
  type        = list(string)
}

variable "is_cluster" {
  description = "Whether monitoring Aurora clusters (true) or RDS instances (false)"
  type        = bool
  default     = false
}

variable "alarm_name_prefix" {
  description = "Prefix for all alarm names"
  type        = string
  default     = "db-alarm"
}

# Alarm Thresholds
variable "cpu_threshold" {
  description = "CPU utilization threshold percentage"
  type        = number
}

variable "memory_threshold" {
  description = "Freeable memory threshold in bytes"
  type        = number
}

variable "latency_threshold" {
  description = "Latency threshold in seconds"
  type        = number
}

# Slack Configuration
variable "slack_webhook_url" {
  description = "Slack incoming webhook URL"
  type        = string
  sensitive   = true
}

variable "slack_channel" {
  description = "Slack channel to send alerts"
  type        = string
}

variable "environment" {
  description = "Environment name (dev/staging/prod)"
  type        = string
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}

variable "free_storage_threshold" {
  type        = number
  default     = 10368709120  # 5 GB in bytes
  description = "Threshold for free storage in bytes"
}
