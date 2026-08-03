# logger.py — saves every conversation to a JSON file

import json
import os
from datetime import datetime

LOG_FILE = "chat_logs.json"

def load_logs():
    """Load existing logs or return empty list"""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    return []

def save_message(role, content, tokens_used=None):
    """Append a single message to the log file"""
    logs = load_logs()
    
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "role": role,
        "content": content
    }
    
    if tokens_used:
        entry["tokens_used"] = tokens_used
    
    logs.append(entry)
    
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

def save_session_divider():
    """Mark the start of a new session in logs"""
    logs = load_logs()
    logs.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "role": "system",
        "content": "--- NEW SESSION STARTED ---"
    })
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)