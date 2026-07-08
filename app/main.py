from datetime import datetime, timezone
import logging

from app.config import NOTIFICATION_WINDOW
from app.discord_webhook import send_match_alert
from app.fifa import get_matches
from app.logger import setup_logging
from app.parser import parse_match
from app.storage import load_sent, save_sent

setup_logging()


def check_matches():
    matches = get_matches()["Results"]
    sent = load_sent()

    logging.info(
        "Retrieved %d matches | Already notified: %d",
        len(matches),
        len(sent),
    )

    now = datetime.now(timezone.utc)

    upcoming = 0
    skipped = 0
    notified = 0

    for raw_match in matches:

        match = parse_match(raw_match)

        if match is None:
            skipped += 1
            continue

        minutes_until_kickoff = (
            match["kickoff"] - now
        ).total_seconds() / 60

        if minutes_until_kickoff < 0:
            skipped += 1
            continue

        upcoming += 1

        if minutes_until_kickoff > NOTIFICATION_WINDOW:
            continue

        if match["id"] in sent:
            logging.info(
                "Already notified: %s vs %s",
                match["home"],
                match["away"],
            )
            continue

        logging.info(
            "Sending notification: %s vs %s (%.1f min)",
            match["home"],
            match["away"],
            minutes_until_kickoff,
        )

        send_match_alert(match)

        sent.add(match["id"])
        save_sent(sent)

        notified += 1

        logging.info(
            "Notification sent successfully."
        )

    logging.info(
        "Finished. Upcoming=%d | Sent=%d | Skipped=%d",
        upcoming,
        notified,
        skipped,
    )


if __name__ == "__main__":
    check_matches()