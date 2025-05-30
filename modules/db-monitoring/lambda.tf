# data "archive_file" "lambda_zip" {
#   type        = "zip"
#   output_path = "${path.module}/lambda.zip"

#   source {
#     content  = <<EOF
# import os
# import json
# import urllib3
# from datetime import datetime, timezone, timedelta

# http = urllib3.PoolManager()

# def lambda_handler(event, context):
#     webhook_url = os.environ["SLACK_WEBHOOK_URL"]
#     slack_channel = os.environ["SLACK_CHANNEL"]
#     environment = os.environ.get("ENVIRONMENT", "unknown")
    
#     sns_message = json.loads(event['Records'][0]['Sns']['Message'])
#     alarm_name = sns_message['AlarmName']
#     db_identifier = alarm_name.split('-')[-1]  # Gets last part of alarm name
    
#     # Australia time with DST (AEST = UTC+10, AEDT = UTC+11)
#     now = datetime.now(timezone.utc)
#     is_dst = now.month in [10,11,12,1,2,3]  # Oct-Mar = Daylight Saving
#     aus_time = now + timedelta(hours=11 if is_dst else 10)
    
#     slack_msg = {
#         "channel": slack_channel,
#         "username": f"AWS {environment} Alert",
#         "icon_emoji": ":postgresql:",
#         "attachments": [{
#             "color": "#FF0000" if sns_message["NewStateValue"] == "ALARM" else "#36A64F",
#             "title": f"{'🚨' if sns_message['NewStateValue'] == 'ALARM' else '✅'} {alarm_name}",
#             "text": f"*Database:* `{db_identifier}`\n*Environment:* {environment}",
#             "fields": [
#                 {
#                     "title": "Details", 
#                     "value": f"```{sns_message['NewStateReason']}```",
#                     "short": False
#                 },
#                 {
#                     "title": "Local Time", 
#                     "value": aus_time.strftime("%Y-%m-%d %H:%M %Z"),
#                     "short": True
#                 }
#             ],
#             "footer": "Investigate in AWS Console → CloudWatch → Alarms",
#             "ts": aus_time.timestamp()
#         }]
#     }
    
#     http.request(
#         "POST", 
#         webhook_url,
#         body=json.dumps(slack_msg),
#         headers={"Content-Type": "application/json"}
#     )
    
#     return {"statusCode": 200}
# EOF
#     filename = "slack_notifier.py"
#   }
# }

# resource "aws_lambda_function" "slack_notifier" {
#   filename      = data.archive_file.lambda_zip.output_path
#   function_name = "${var.environment}-db-alerts-notifier"
#   role          = aws_iam_role.lambda_exec.arn
#   handler       = "slack_notifier.lambda_handler"
#   runtime       = "python3.9"
#   timeout       = 10
  
#   environment {
#     variables = {
#       SLACK_WEBHOOK_URL = var.slack_webhook_url
#       SLACK_CHANNEL     = var.slack_channel
#       ENVIRONMENT       = var.environment
#     }
#   }
  
#   tags = var.tags
# }




# data "archive_file" "lambda_zip" {
#   type        = "zip"
#   output_path = "${path.module}/lambda.zip"

#   source {
#     content  = <<EOF
# import os
# import json
# import urllib3
# from datetime import datetime, timezone, timedelta

# http = urllib3.PoolManager()

# def format_bytes(size):
#     """Convert bytes to human-readable format"""
#     for unit in ['B', 'KB', 'MB', 'GB']:
#         if size < 1024.0:
#             return f"{size:.1f} {unit}"
#         size /= 1024.0
#     return f"{size:.1f} TB"

# def get_australia_time():
#     """Get current Australia time with DST handling"""
#     now = datetime.now(timezone.utc)
#     is_dst = now.month in [10, 11, 12, 1, 2, 3]  # Oct-Mar is DST
#     return now + timedelta(hours=11 if is_dst else 10)

# def lambda_handler(event, context):
#     webhook_url = os.environ["SLACK_WEBHOOK_URL"]
#     slack_channel = os.environ["SLACK_CHANNEL"]
#     environment = os.environ.get("ENVIRONMENT", "unknown")
    
#     sns_message = json.loads(event['Records'][0]['Sns']['Message'])
#     alarm_name = sns_message['AlarmName']
#     alarm_desc = sns_message.get('AlarmDescription', 'Database alert')
#     new_state = sns_message['NewStateValue']
#     reason = sns_message['NewStateReason']
    
#     # Extract metric info
#     is_memory_alarm = 'FreeableMemory' in alarm_name
#     db_identifier = alarm_name.split('-')[-1]
#     aus_time = get_australia_time()
    
#     # Format message based on alarm type
#     if is_memory_alarm:
#         # Extract memory value from reason
#         memory_value = float(reason.split('datapoint(s) (')[1].split(')')[0])
#         formatted_value = format_bytes(memory_value)
#         threshold_value = format_bytes(float(reason.split('threshold (')[1].split(')')[0]))
        
#         title = f"🚨 LOW MEMORY - {db_identifier}"
#         details = f"""• Current memory: {formatted_value}
# • Threshold: {threshold_value}
# • Database: {db_identifier}"""
#     else:
#         # CPU alarm
#         cpu_value = float(reason.split('datapoint(s) (')[1].split(')')[0])
#         threshold = float(reason.split('threshold (')[1].split(')')[0])
        
#         title = f"🚨 HIGH CPU - {db_identifier}"
#         details = f"""• Current CPU: {cpu_value:.1f}%
# • Threshold: {threshold}%
# • Database: {db_identifier}"""

#     slack_msg = {
#         "channel": slack_channel,
#         "username": f"AWS {environment} Alert",
#         "icon_emoji": ":warning:",
#         "attachments": [{
#             "color": "#FF0000" if new_state == "ALARM" else "#36A64F",
#             "title": title,
#             "text": alarm_desc,
#             "fields": [
#                 {
#                     "title": "Details",
#                     "value": details,
#                     "short": False
#                 },
#                 {
#                     "title": "Environment",
#                     "value": environment,
#                     "short": True
#                 },
#                 {
#                     "title": "Local Time",
#                     "value": aus_time.strftime("%a, %d %b %Y %H:%M %Z"),
#                     "short": True
#                 }
#             ],
#             "footer": "Investigate in CloudWatch → Alarms",
#             "ts": aus_time.timestamp()
#         }]
#     }
    
#     try:
#         response = http.request(
#             "POST",
#             webhook_url,
#             body=json.dumps(slack_msg),
#             headers={"Content-Type": "application/json"}
#         )
#         if response.status != 200:
#             print(f"Slack API error: {response.data.decode('utf-8')}")
#     except Exception as e:
#         print(f"Error sending to Slack: {str(e)}")
#         raise

#     return {"statusCode": 200}
# EOF
#     filename = "slack_notifier.py"
#   }
# }










# data "archive_file" "lambda_zip" {
#   type        = "zip"
#   output_path = "${path.module}/lambda.zip"

#   source {
#     content  = <<EOF
# import os
# import json
# import urllib3
# from datetime import datetime, timezone, timedelta

# http = urllib3.PoolManager()

# def format_bytes(size):
#     """Convert bytes to human-readable format"""
#     for unit in ['B', 'KB', 'MB', 'GB']:
#         if size < 1024.0:
#             return f"{size:.1f} {unit}"
#         size /= 1024.0
#     return f"{size:.1f} TB"

# def get_australia_time():
#     """Get current Australia time with DST handling"""
#     now = datetime.now(timezone.utc)
#     is_dst = now.month in [10, 11, 12, 1, 2, 3]  # Oct-Mar is DST
#     return now + timedelta(hours=11 if is_dst else 10)

# def lambda_handler(event, context):
#     webhook_url = os.environ["SLACK_WEBHOOK_URL"]
#     slack_channel = os.environ["SLACK_CHANNEL"]
#     environment = os.environ.get("ENVIRONMENT", "unknown")
    
#     sns_message = json.loads(event['Records'][0]['Sns']['Message'])
#     alarm_name = sns_message['AlarmName']
#     alarm_desc = sns_message.get('AlarmDescription', 'Database alert')
#     new_state = sns_message['NewStateValue']
#     reason = sns_message['NewStateReason']
    
#     # Extract metric info
#     is_memory_alarm = 'FreeableMemory' in alarm_name
#     db_identifier = alarm_name.split('-')[-1]
#     aus_time = get_australia_time()
    
#     # Format message based on alarm type
#     if is_memory_alarm:
#         # Extract memory value from reason
#         try:
#             memory_str = reason.split('datapoint(s) (')[1].split(')')[0]
#             memory_value = float(memory_str.strip('% '))
#         except (IndexError, ValueError):
#             memory_value = -1.0

#         try:
#             threshold_str = reason.split('threshold (')[1].split(')')[0]
#             threshold_value = float(threshold_str.strip('% '))
#         except (IndexError, ValueError):
#             threshold_value = -1.0

#         formatted_value = format_bytes(memory_value)
#         threshold_formatted = format_bytes(threshold_value)

#         title = f"🚨 LOW MEMORY - {db_identifier}"
#         details = f"""• Current memory: {formatted_value}
# • Threshold: {threshold_formatted}
# • Database: {db_identifier}"""
#     else:
#         # CPU alarm
#         try:
#             cpu_str = reason.split('datapoint(s) (')[1].split(')')[0]
#             cpu_value = float(cpu_str.strip('% '))
#         except (IndexError, ValueError):
#             cpu_value = -1.0

#         try:
#             threshold_str = reason.split('threshold (')[1].split(')')[0]
#             threshold = float(threshold_str.strip('% '))
#         except (IndexError, ValueError):
#             threshold = -1.0

#         title = f"🚨 HIGH CPU - {db_identifier}"
#         details = f"""• Current CPU: {cpu_value:.1f}%
# • Threshold: {threshold}%
# • Database: {db_identifier}"""

#     slack_msg = {
#         "channel": slack_channel,
#         "username": f"AWS {environment} Alert",
#         "icon_emoji": ":warning:",
#         "attachments": [{
#             "color": "#FF0000" if new_state == "ALARM" else "#36A64F",
#             "title": title,
#             "text": alarm_desc,
#             "fields": [
#                 {
#                     "title": "Details",
#                     "value": details,
#                     "short": False
#                 },
#                 {
#                     "title": "Environment",
#                     "value": environment,
#                     "short": True
#                 },
#                 {
#                     "title": "Local Time",
#                     "value": aus_time.strftime("%a, %d %b %Y %H:%M %Z"),
#                     "short": True
#                 }
#             ],
#             "footer": "Investigate in CloudWatch → Alarms",
#             "ts": aus_time.timestamp()
#         }]
#     }
    
#     try:
#         response = http.request(
#             "POST",
#             webhook_url,
#             body=json.dumps(slack_msg),
#             headers={"Content-Type": "application/json"}
#         )
#         if response.status != 200:
#             print(f"Slack API error: {response.data.decode('utf-8')}")
#     except Exception as e:
#         print(f"Error sending to Slack: {str(e)}")
#         raise

#     return {"statusCode": 200}
# EOF
#     filename = "slack_notifier.py"
#   }
# }



data "archive_file" "lambda_zip" {
  type        = "zip"
  output_path = "${path.module}/lambda.zip"

  source {
    content  = <<EOF
import os
import json
import urllib3
from datetime import datetime, timezone, timedelta

http = urllib3.PoolManager()

def format_bytes(size):
    """Convert bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"

def get_australia_time():
    """Get current Australia time with DST handling"""
    now = datetime.now(timezone.utc)
    is_dst = now.month in [10, 11, 12, 1, 2, 3]  # Oct-Mar is DST
    return now + timedelta(hours=11 if is_dst else 10)

def lambda_handler(event, context):
    webhook_url = os.environ["SLACK_WEBHOOK_URL"]
    slack_channel = os.environ["SLACK_CHANNEL"]
    environment = os.environ.get("ENVIRONMENT", "unknown")
    
    sns_message = json.loads(event['Records'][0]['Sns']['Message'])
    alarm_name = sns_message['AlarmName']
    alarm_desc = sns_message.get('AlarmDescription', 'Database alert')
    new_state = sns_message['NewStateValue']
    reason = sns_message['NewStateReason']

    # Extract metric name and DB identifier
    trigger = sns_message.get("Trigger", {})
    metric_name = trigger.get("MetricName", "")
    is_memory_alarm = metric_name == "FreeableMemory"

    dimensions = trigger.get("Dimensions", [])
    db_identifier = next((d["value"] for d in dimensions if d["name"] == "DBInstanceIdentifier"), "unknown-db")

    aus_time = get_australia_time()

    # Format message based on alarm type
    if is_memory_alarm:
        # Extract memory value from reason
        try:
            memory_str = reason.split('datapoint(s) (')[1].split(')')[0]
            memory_value = float(memory_str.strip('% '))
        except (IndexError, ValueError):
            memory_value = -1.0

        try:
            threshold_str = reason.split('threshold (')[1].split(')')[0]
            threshold_value = float(threshold_str.strip('% '))
        except (IndexError, ValueError):
            threshold_value = -1.0

        formatted_value = format_bytes(memory_value)
        threshold_formatted = format_bytes(threshold_value)

        title = f"🚨 LOW MEMORY - {db_identifier}"
        details = f"""• Current memory: {formatted_value}
• Threshold: {threshold_formatted}
• Database: {db_identifier}"""
    else:
        # CPU alarm
        try:
            cpu_str = reason.split('datapoint(s) (')[1].split(')')[0]
            cpu_value = float(cpu_str.strip('% '))
        except (IndexError, ValueError):
            cpu_value = -1.0

        try:
            threshold_str = reason.split('threshold (')[1].split(')')[0]
            threshold = float(threshold_str.strip('% '))
        except (IndexError, ValueError):
            threshold = -1.0

        title = f"🚨 HIGH CPU - {db_identifier}"
        details = f"""• Current CPU: {cpu_value:.1f}%
• Threshold: {threshold}%
• Database: {db_identifier}"""

    slack_msg = {
        "channel": slack_channel,
        "username": f"AWS {environment} Alert",
        "icon_emoji": ":warning:",
        "attachments": [{
            "color": "#FF0000" if new_state == "ALARM" else "#36A64F",
            "title": title,
            "text": alarm_desc,
            "fields": [
                {
                    "title": "Details",
                    "value": details,
                    "short": False
                },
                {
                    "title": "Environment",
                    "value": environment,
                    "short": True
                },
                {
                    "title": "Local Time",
                    "value": aus_time.strftime("%a, %d %b %Y %H:%M %Z"),
                    "short": True
                }
            ],
            "footer": "Investigate in CloudWatch → Alarms",
            "ts": aus_time.timestamp()
        }]
    }

    try:
        response = http.request(
            "POST",
            webhook_url,
            body=json.dumps(slack_msg),
            headers={"Content-Type": "application/json"}
        )
        if response.status != 200:
            print(f"Slack API error: {response.data.decode('utf-8')}")
    except Exception as e:
        print(f"Error sending to Slack: {str(e)}")
        raise

    return {"statusCode": 200}
EOF
    filename = "slack_notifier.py"
  }
}





resource "aws_lambda_function" "slack_notifier" {
  filename      = data.archive_file.lambda_zip.output_path
  function_name = "${var.environment}-db-alerts-notifier"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "slack_notifier.lambda_handler"
  runtime       = "python3.9"
  timeout       = 10
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  
  environment {
    variables = {
      SLACK_WEBHOOK_URL = var.slack_webhook_url
      SLACK_CHANNEL     = var.slack_channel
      ENVIRONMENT       = var.environment
    }
  }
  
  tags = var.tags
}
