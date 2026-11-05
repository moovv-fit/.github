import sys
import json
import re

try:
    data = json.load(sys.stdin)
    args = data.get("toolCall", {}).get("args", {})
    cmd = args.get("CommandLine", "")
    
    # Destructive git commands check
    destructive_pattern = r"git\s+(push\s+.*(--force|-f)|reset\s+--hard|clean\s+-[a-zA-Z]*f|branch\s+-D)"
    if re.search(destructive_pattern, cmd):
        print(json.dumps({
            "decision": "ask",
            "reason": f"Destructive git command detected: '{cmd}'. Confirmation required."
        }))
    else:
        print(json.dumps({"decision": "allow"}))
except Exception:
    print(json.dumps({"decision": "allow"}))
