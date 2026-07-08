import logging

import requests

from app.config import DISCORD_WEBHOOK
from app.flags import get_flag
from app.http import session


def send_match_alert(match):
    """
    Send a Discord notification for an upcoming FIFA World Cup match.
    """

    unix_time = int(match["kickoff"].timestamp())

    home_flag = get_flag(match["home"])
    away_flag = get_flag(match["away"])

    payload = {
        "content": "@everyone",
        "embeds": [
            {
                "title": "⚽ FIFA World Cup Match Starting Soon",
                "description": (
                    f"{home_flag} **{match['home']}**\n"
                    f"🆚\n"
                    f"{away_flag} **{match['away']}**"
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
                        "value": (
                            f"<t:{unix_time}:F>\n"
                            f"<t:{unix_time}:R>"
                        ),
                        "inline": True,
                    },
                ],
                "footer": {
                    "text": "FIFA World Cup 2026",
                },
            }
        ],
    }

    try:
        response = session.post(
            DISCORD_WEBHOOK,
            json=payload,
            timeout=15,
        )

        response.raise_for_status()

        logging.info(
            "Discord notification delivered successfully."
        )

    except requests.exceptions.Timeout:
        logging.exception(
            "Discord webhook request timed out."
        )
        raise

    except requests.exceptions.HTTPError:
        logging.exception(
            "Discord returned %s\n%s",
            response.status_code,
            response.text,
        )
        raise

    except requests.exceptions.RequestException:
        logging.exception(
            "Unable to reach the Discord webhook."
        )
        raise