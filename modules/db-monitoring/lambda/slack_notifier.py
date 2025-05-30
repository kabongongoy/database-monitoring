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
#     environment = os.environ.get("ENVIRONMENT", "support")

#     sns_message = json.loads(event['Records'][0]['Sns']['Message'])
#     alarm_name = sns_message.get('AlarmName', 'UnknownAlarm')
#     alarm_desc = sns_message.get('AlarmDescription', 'Database alert')
#     new_state = sns_message.get('NewStateValue', 'UNKNOWN')
#     reason = sns_message.get('NewStateReason', '')

#     # Extract trigger info for metric and DB identifier
#     trigger = sns_message.get("Trigger", {})
#     metric_name = trigger.get("MetricName", "UnknownMetric")
#     dimensions = trigger.get("Dimensions", [])
#     db_identifier = "unknown"
#     for d in dimensions:
#         if d.get("name") in ["DBInstanceIdentifier", "DBClusterIdentifier"]:
#             db_identifier = d.get("value")
#             break

#     # Parse values safely
#     try:
#         value = float(reason.split('datapoint(s) (')[1].split(')')[0])
#         threshold = float(reason.split('threshold (')[1].split(')')[0])
#     except Exception:
#         value = None
#         threshold = None

#     aus_time = get_australia_time()

#     # Build message based on metric
#     if metric_name == "FreeableMemory" and value is not None and threshold is not None:
#         formatted_value = format_bytes(value)
#         formatted_threshold = format_bytes(threshold)
#         title = f"🚨 LOW MEMORY - {db_identifier}"
#         details = f"""• Memory: {formatted_value}
# • Threshold: {formatted_threshold}
# • Database: {db_identifier}"""

#     elif metric_name == "FreeStorageSpace" and value is not None and threshold is not None:
#         formatted_value = format_bytes(value)
#         formatted_threshold = format_bytes(threshold)
#         title = f"🚨 LOW STORAGE - {db_identifier}"
#         details = f"""• Storage: {formatted_value}
# • Threshold: {formatted_threshold}
# • Database: {db_identifier}"""

#     elif metric_name == "CPUUtilization" and value is not None and threshold is not None:
#         title = f"🚨 HIGH CPU - {db_identifier}"
#         details = f"""• CPU: {value:.1f}%
# • Threshold: {threshold}%
# • Database: {db_identifier}"""

#     elif metric_name == "Deadlocks" and value is not None and threshold is not None:
#         title = f"🚨 DEADLOCKS DETECTED - {db_identifier}"
#         details = f"""• Deadlocks: {value:.1f}
# • Threshold: {threshold}
# • Database: {db_identifier}"""

#     elif metric_name == "Latency" and value is not None and threshold is not None:
#         title = f"🚨 HIGH LATENCY - {db_identifier}"
#         details = f"""• Latency: {value:.2f} ms
# • Threshold: {threshold} ms
# • Database: {db_identifier}"""

#     else:
#         # Fallback for unknown metrics or parse errors
#         title = f"⚠️ ALERT - {metric_name} - {db_identifier}"
#         if value is not None and threshold is not None:
#             details = f"""• Value: {value}
# • Threshold: {threshold}
# • Database: {db_identifier}"""
#         else:
#             details = f"""• Unable to parse metric values.
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
#             "ts": int(aus_time.timestamp())
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

#___________________


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
#     alarm_name = sns_message.get('AlarmName', 'UnknownAlarm')
#     alarm_desc = sns_message.get('AlarmDescription', 'Database alert')
#     new_state = sns_message.get('NewStateValue', 'UNKNOWN')
#     trigger = sns_message.get("Trigger", {})

#     metric_name = trigger.get("MetricName", "UnknownMetric")
#     value = trigger.get("MetricValue")
#     threshold = trigger.get("Threshold")

#     # Extract DB identifier
#     dimensions = trigger.get("Dimensions", [])
#     db_identifier = "unknown"
#     for d in dimensions:
#         if d.get("name") in ["DBInstanceIdentifier", "DBClusterIdentifier"]:
#             db_identifier = d.get("value")
#             break

#     aus_time = get_australia_time()

#     # Format alert details
#     if metric_name == "FreeableMemory" and value is not None and threshold is not None:
#         formatted_value = format_bytes(value)
#         formatted_threshold = format_bytes(threshold)
#         title = f"🚨 LOW MEMORY - {db_identifier}"
#         details = f"""• Memory: {formatted_value}
# • Threshold: {formatted_threshold}
# • Database: {db_identifier}"""

#     elif metric_name == "FreeStorageSpace" and value is not None and threshold is not None:
#         formatted_value = format_bytes(value)
#         formatted_threshold = format_bytes(threshold)
#         title = f"🚨 LOW STORAGE - {db_identifier}"
#         details = f"""• Storage: {formatted_value}
# • Threshold: {formatted_threshold}
# • Database: {db_identifier}"""

#     elif metric_name == "CPUUtilization" and value is not None and threshold is not None:
#         title = f"🚨 HIGH CPU - {db_identifier}"
#         details = f"""• CPU: {value:.1f}%
# • Threshold: {threshold}%
# • Database: {db_identifier}"""

#     elif metric_name == "Deadlocks" and value is not None and threshold is not None:
#         title = f"🚨 DEADLOCKS DETECTED - {db_identifier}"
#         details = f"""• Deadlocks: {value:.1f}
# • Threshold: {threshold}
# • Database: {db_identifier}"""

#     elif metric_name == "Latency" and value is not None and threshold is not None:
#         title = f"🚨 HIGH LATENCY - {db_identifier}"
#         details = f"""• Latency: {value:.2f} ms
# • Threshold: {threshold} ms
# • Database: {db_identifier}"""

#     else:
#         # Fallback for unknown metrics or missing values
#         title = f"⚠️ ALERT - {metric_name} - {db_identifier}"
#         if value is not None and threshold is not None:
#             details = f"""• Value: {value}
# • Threshold: {threshold}
# • Database: {db_identifier}"""
#         else:
#             details = f"""• Unable to parse metric values.
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
#             "ts": int(aus_time.timestamp())
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
    environment = os.environ.get("ENVIRONMENT", "Support")

    sns_message = json.loads(event['Records'][0]['Sns']['Message'])
    alarm_name = sns_message.get('AlarmName', 'UnknownAlarm')
    alarm_desc = sns_message.get('AlarmDescription', 'Database alert')
    new_state = sns_message.get('NewStateValue', 'UNKNOWN')
    trigger = sns_message.get("Trigger", {})

    metric_name = trigger.get("MetricName", "UnknownMetric")
    value = trigger.get("MetricValue")
    threshold = trigger.get("Threshold")

    # Extract DB identifier
    dimensions = trigger.get("Dimensions", [])
    db_identifier = "unknown"
    for d in dimensions:
        if d.get("name") in ["DBInstanceIdentifier", "DBClusterIdentifier"]:
            db_identifier = d.get("value")
            break

    aus_time = get_australia_time()

    # Format alert details
    if metric_name == "FreeableMemory" and value is not None and threshold is not None:
        formatted_value = format_bytes(value)
        formatted_threshold = format_bytes(threshold)
        title = f"🚨 LOW MEMORY - {db_identifier}"
        details = f"""• Memory: {formatted_value}
• Threshold: {formatted_threshold}
• Database: {db_identifier}"""

    elif metric_name == "FreeStorageSpace" and value is not None and threshold is not None:
        formatted_value = format_bytes(value)
        formatted_threshold = format_bytes(threshold)
        title = f"🚨 LOW STORAGE - {db_identifier}"
        details = f"""• Storage: {formatted_value}
• Threshold: {formatted_threshold}
• Database: {db_identifier}"""

    elif metric_name == "CPUUtilization" and value is not None and threshold is not None:
        title = f"🚨 HIGH CPU - {db_identifier}"
        details = f"""• CPU: {value:.1f}%
• Threshold: {threshold}%
• Database: {db_identifier}"""

    elif metric_name == "Deadlocks" and value is not None and threshold is not None:
        title = f"🚨 DEADLOCKS DETECTED - {db_identifier}"
        details = f"""• Deadlocks: {value:.1f}
• Threshold: {threshold}
• Database: {db_identifier}"""

    elif metric_name == "Latency" and value is not None and threshold is not None:
        title = f"🚨 HIGH LATENCY - {db_identifier}"
        details = f"""• Latency: {value:.2f} ms
• Threshold: {threshold} ms
• Database: {db_identifier}"""

    else:
        # Fallback for unknown metrics or missing values
        title = f"⚠️ ALERT - {metric_name} - {db_identifier}"
        detail_lines = [f"• Database: {db_identifier}"]
        if value is not None:
            detail_lines.insert(0, f"• Value: {value}")
        if threshold is not None:
            detail_lines.insert(1, f"• Threshold: {threshold}")
        details = "\n".join(detail_lines)

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
            "ts": int(aus_time.timestamp())
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
