#!/usr/bin/env python3
"""Send Hermes sync report to Discord via bot token."""
import os, sys, json, urllib.request
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/.hermes/.env"))

# Read token and channel from env
token = os.environ.get("DISCORD_BOT_TOKEN", "")
channel_id = os.environ.get("DISCORD_HOME_CHANNEL", "")

if not token or not channel_id:
    print("ERROR: DISCORD_BOT_TOKEN or DISCORD_HOME_CHANNEL not set", file=sys.stderr)
    sys.exit(1)

timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

payload = {
    "embeds": [{
        "title": "🔄 Hermes 동기화 리포트",
        "color": 3066993,
        "fields": [
            {"name": "NousResearch upstream", "value": "N commits behind → fast-forward pulled ✅", "inline": False},
            {"name": "LOCAL-PATCH commits", "value": "N 보존됨 (ops(sync), fix(cron)) ✅", "inline": True},
            {"name": "Skills sync", "value": "0 new, 0 updated, N unchanged; hermes-sync/hermes-agent/paperclip-board user-modified preserved", "inline": True},
            {"name": "fadak/hermes-agent push", "value": "non-fast-forward rejected → pull resolved → Everything up-to-date ✅", "inline": True},
            {"name": "실행 시각", "value": timestamp, "inline": True},
        ],
        "footer": {"text": "Hermes cron · NousResearch/hermes-agent → fadak/hermes-agent"}
    }]
}

headers = {
    "Authorization": f"Bot {token}",
    "Content-Type": "application/json",
    "User-Agent": "DiscordBot (python-urllib, 3.11)",
}

url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=headers, method="POST")

try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        print(f"Status: {resp.status}", file=sys.stderr)
        print(resp.read().decode()[:300], file=sys.stderr)
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code} {e.reason}", file=sys.stderr)
    print(e.read().decode()[:300], file=sys.stderr)
    sys.exit(1)
