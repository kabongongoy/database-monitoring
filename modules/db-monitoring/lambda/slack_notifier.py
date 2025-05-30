# import os
# import json
# import urllib3
# from datetime import datetime
# import pytz  # For Australia timezone

# http = urllib3.PoolManager()

# def lambda_handler(event, context):
#     # Get configuration from environment variables
#     webhook_url = os.environ["SLACK_WEBHOOK_URL"]
#     slack_channel = os.environ["SLACK_CHANNEL"]
#     environment = os.environ.get("ENVIRONMENT", "unknown")
    
#     # Parse the CloudWatch alarm
#     sns_message = json.loads(event["Records"][0]["Sns"]["Message"])
    
#     # Australia timezone (auto-adjusts for DST)
#     australia_tz = pytz.timezone('Australia/Sydney')
#     timestamp = datetime.now(australia_tz).strftime("%Y-%m-%d %H:%M %Z")
    
#     # Format alarm details
#     alarm_name = format_alarm_name(sns_message["AlarmName"])
#     alarm_description = sns_message.get("AlarmDescription", "Database monitoring alert")
#     new_state = sns_message["NewStateValue"]
#     reason = sns_message["NewStateReason"]
    
#     # Determine alert color and icon
#     color, emoji = {
#         "ALARM": ("#FF0000", ":red_circle:"),
#         "OK": ("#36A64F", ":large_green_circle:"),
#         "INSUFFICIENT_DATA": ("#FFA500", ":warning:")
#     }.get(new_state, ("#764FA5", ":question:"))
    
#     # Build Slack message
#     slack_payload = {
#         "channel": slack_channel,
#         "username": "AWS Database Monitor",
#         "icon_emoji": ":aws:",
#         "attachments": [{
#             "color": color,
#             "title": f"{emoji} {alarm_name} - {new_state}",
#             "text": f"*{alarm_description}*",
#             "fields": [
#                 {"title": "Environment", "value": environment, "short": True},
#                 {"title": "Status", "value": new_state, "short": True},
#                 {"title": "Time (AEST/AEDT)", "value": timestamp, "short": True},
#                 {
#                     "title": "Details", 
#                     "value": f"```{reason}```",  # Removed Jira link
#                     "short": False
#                 }
#             ],
#             "footer": "Investigation path: CloudWatch → RDS Metrics",
#             "ts": datetime.now(australia_tz).timestamp()
#         }]
#     }
    
#     # Send to Slack
#     try:
#         response = http.request(
#             "POST",
#             webhook_url,
#             body=json.dumps(slack_payload),
#             headers={"Content-Type": "application/json"}
#         )
#         if response.status != 200:
#             raise Exception(f"Slack API error: {response.data.decode('utf-8')}")
#     except Exception as e:
#         print(f"Error sending to Slack: {str(e)}")
#         raise

#     return {"statusCode": 200}

# def format_alarm_name(raw_name):
#     """Convert alarm names to human-readable format"""
#     return (raw_name
#             .replace("_", " ")
#             .replace("-", " ")
#             .title()
#             .replace("Cpu", "CPU")
#             .replace("Db", "DB")
#             .replace("Rds", "RDS"))



#----------------------

import os
import json
import urllib3
from datetime import datetime, timezone, timedelta

http = urllib3.PoolManager()

def lambda_handler(event, context):
    # Get configuration from environment variables
    webhook_url = os.environ["SLACK_WEBHOOK_URL"]
    slack_channel = os.environ["SLACK_CHANNEL"]
    environment = os.environ.get("ENVIRONMENT", "unknown")
    
    # Parse the CloudWatch alarm
    sns_message = json.loads(event["Records"][0]["Sns"]["Message"])
    
    # Calculate Australia time (AEST = UTC+10, AEDT = UTC+11)
    australia_offset = 11 if is_daylight_saving() else 10
    aus_time = datetime.now(timezone.utc) + timedelta(hours=australia_offset)
    timestamp = aus_time.strftime("%Y-%m-%d %H:%M (AEST/AEDT)")
    
    # Format alarm details
    alarm_name = format_alarm_name(sns_message["AlarmName"])
    alarm_description = sns_message.get("AlarmDescription", "Database alert")
    new_state = sns_message["NewStateValue"]
    reason = sns_message["NewStateReason"]
    
    # Determine alert color and icon
    if new_state == "ALARM":
        color = "#FF0000"  # Red
        emoji = ":red_circle:"
    elif new_state == "OK":
        color = "#36A64F"  # Green
        emoji = ":large_green_circle:"
    else:  # INSUFFICIENT_DATA
        color = "#FFA500"  # Orange
        emoji = ":warning:"
    
    # Build Slack message
    slack_payload = {
        "channel": slack_channel,
        "username": "AWS Database Monitor",
        "icon_emoji": ":aws:",
        "attachments": [{
            "color": color,
            "title": f"{emoji} {alarm_name} - {new_state}",
            "text": f"*{alarm_description}*",
            "fields": [
                {"title": "Environment", "value": environment, "short": True},
                {"title": "Status", "value": new_state, "short": True},
                {"title": "Time", "value": timestamp, "short": True},
                {"title": "Details", "value": f"```{reason}```", "short": False}
            ],
            "footer": "Investigation: CloudWatch → RDS Metrics",
            "ts": aus_time.timestamp()
        }]
    }
    
    # Send to Slack
    try:
        response = http.request(
            "POST",
            webhook_url,
            body=json.dumps(slack_payload),
            headers={"Content-Type": "application/json"}
        )
        if response.status != 200:
            raise Exception(f"Slack API error: {response.data.decode('utf-8')}")
    except Exception as e:
        print(f"Error sending to Slack: {str(e)}")
        raise

    return {"statusCode": 200}

def is_daylight_saving():
    """Check if daylight saving is active in Australia (first Sun Oct to first Sun Apr)"""
    now = datetime.now(timezone.utc)
    year = now.year
    # DST starts first Sunday in October
    october = datetime(year, 10, 1, tzinfo=timezone.utc)
    dst_start = october + timedelta(days=(6 - october.weekday()) % 7)
    # DST ends first Sunday in April
    april = datetime(year, 4, 1, tzinfo=timezone.utc)
    dst_end = april + timedelta(days=(6 - april.weekday()) % 7)
    return dst_start <= now < dst_end

def format_alarm_name(raw_name):
    """Convert alarm names to human-readable format"""
    name = raw_name.replace("_", " ").replace("-", " ").title()
    return name.replace("Cpu", "CPU").replace("Db", "DB").replace("Rds", "RDS")
