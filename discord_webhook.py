import json
import requests

from config import DISCORD_WEBHOOK


def send_match_alert(match):
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
                    "text": "FIFA World Cup 2026",
                },
            }
        ],
    }

    print("\n========== SENDING TO DISCORD ==========")
    print("Webhook:")
    print(DISCORD_WEBHOOK)
    print("\nPayload:")
    print(json.dumps(payload, indent=4))

    try:
        response = requests.post(DISCORD_WEBHOOK, json=payload)

        print("\nStatus Code:", response.status_code)
        print("Response Body:")
        print(response.text)

        response.raise_for_status()

        print("\n✅ Discord notification sent successfully.\n")

    except Exception as e:
        print("\n❌ Discord request failed")
        print(e)