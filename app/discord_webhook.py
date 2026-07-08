import logging

import requests

from app.config import DISCORD_WEBHOOK
from app.flags import get_flag


def send_match_alert(match):
    """Send a Discord notification for an upcoming match."""

    unix_time = int(match["kickoff"].timestamp())

    payload = {
        "content": "@everyone",
        "embeds": [
            {
                "title": "⚽ FIFA World Cup Match Starting Soon",
                "description": (
                    f"**{match['home']}**\n"
                    f"🆚\n"
                    f"**{match['away']}**"
                ),
                "color": 3447003,
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
                ],
                "footer": {
                    "text": "FIFA World Cup 2026"
                },
            }
        ],
    }

    try:
        response = requests.post(
            DISCORD_WEBHOOK,
            json=payload,
            timeout=15,
        )

        response.raise_for_status()

        logging.info(
            "Discord notification delivered successfully."
        )

    except requests.exceptions.Timeout:
        logging.error(
            "Discord webhook request timed out."
        )
        raise

    except requests.exceptions.HTTPError:
        logging.error(
            "Discord returned %s: %s",
            response.status_code,
            response.text,
        )
        raise

    except requests.exceptions.RequestException as exc:
        logging.error(
            "Failed to send Discord notification: %s",
            exc,
        )
        raise