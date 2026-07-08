import logging

import requests

from app.config import DISCORD_WEBHOOK
from app.flags import get_flag

LOGO_URL = (
    "https://raw.githubusercontent.com/"
    "Tixtor710/Score-notifier-webhook/main/"
    "assets/world-cup-logo.png"
)


def send_match_alert(match):
    """Send a Discord notification for an upcoming World Cup match."""

    unix_time = int(match["kickoff"].timestamp())

    payload = {
        "content": "@everyone",
        "embeds": [
            {
                "title": "🏆 FIFA WORLD CUP 2026",
                "description": (
    f"# {get_flag(match['home'])} {match['home']}\n"
    f"## 🆚\n"
    f"# {get_flag(match['away'])} {match['away']}\n\n"
    "### Match starts soon!"
),
                "color": 0xD4AF37,
                "thumbnail": {
                    "url": LOGO_URL
                },
                "fields": [
                    {
                        "name": "🏟 Stadium",
                        "value": match["stadium"],
                        "inline": False,
                    },
                    {
                        "name": "📍 City",
                        "value": match["city"],
                        "inline": True,
                    },
                    {
                        "name": "🕒 Kickoff",
                        "value": f"<t:{unix_time}:F>",
                        "inline": True,
                    },
                    {
                        "name": "⏳ Starts In",
                        "value": f"<t:{unix_time}:R>",
                        "inline": True,
                    },
                ],
                "footer": {
                    "text": "Automated Match Notification • FIFA World Cup 2026"
                },
                "timestamp": match["kickoff"].isoformat(),
            }
        ],
        "allowed_mentions": {
            "parse": ["everyone"]
        },
    }

    response = requests.post(
        DISCORD_WEBHOOK,
        json=payload,
        timeout=10,
    )

    response.raise_for_status()

    logging.info(
        "Discord notification sent for %s vs %s.",
        match["home"],
        match["away"],
    )