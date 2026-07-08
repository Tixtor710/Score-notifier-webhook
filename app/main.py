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
        "Retrieved %d matches from FIFA API.",
        len(matches),
    )

    logging.info(
        "Loaded %d previously sent matches.",
        len(sent),
    )

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

        if minutes_until_kickoff < 0:
            continue

        if minutes_until_kickoff > NOTIFICATION_WINDOW:
            continue

        if match["id"] in sent:
            logging.info(
                "Already notified for %s vs %s.",
                match["home"],
                match["away"],
            )
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

    logging.info(
        "Finished checking all matches."
    )