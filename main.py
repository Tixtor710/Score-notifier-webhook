from datetime import datetime, timezone
import logging

from fifa import get_matches
from parser import parse_match
from discord_webhook import send_match_alert
from storage import load_sent, save_sent


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

matches = get_matches()["Results"]
sent = load_sent()

logging.info("Loaded %d previously sent matches.", len(sent))

now = datetime.now(timezone.utc)

for raw_match in matches:

    match = parse_match(raw_match)

    if match is None:
        continue

    minutes_until_kickoff = (
        match["kickoff"] - now
    ).total_seconds() / 60

    logging.info(
        "%s vs %s (%.1f minutes)",
        match["home"],
        match["away"],
        minutes_until_kickoff,
    )

    # Ignore matches that have already finished
    if minutes_until_kickoff < 0:
        continue

    # Ignore matches more than 30 minutes away
    if minutes_until_kickoff > 30:
        continue

    # Ignore matches we've already notified
    if match["id"] in sent:
        continue

    logging.info(
        "Sending notification for %s vs %s...",
        match["home"],
        match["away"],
    )

    send_match_alert(match)

    sent.add(match["id"])
    save_sent(sent)

    logging.info(
        "Notification sent successfully."
    )