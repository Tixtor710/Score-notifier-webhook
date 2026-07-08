import json
import logging
from pathlib import Path


FILE = Path("sent_matches.json")


def load_sent():
    """
    Load previously notified match IDs.
    """

    if not FILE.exists():
        logging.warning(
            "sent_matches.json not found. Creating a new one."
        )

        save_sent(set())

        return set()

    try:
        with open(FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        logging.info(
            "Loaded %d sent matches.",
            len(data),
        )

        return set(data)

    except json.JSONDecodeError:
        logging.error(
            "sent_matches.json is corrupted. Resetting file."
        )

        save_sent(set())

        return set()

    except Exception as exc:
        logging.exception(
            "Unable to read sent_matches.json: %s",
            exc,
        )

        return set()


def save_sent(sent):
    """
    Save notified match IDs.
    """

    try:
        with open(FILE, "w", encoding="utf-8") as file:
            json.dump(
                sorted(sent),
                file,
                indent=4,
            )

    except Exception as exc:
        logging.exception(
            "Unable to save sent_matches.json: %s",
            exc,
        )