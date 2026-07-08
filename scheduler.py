import logging
import time

import schedule

from app.config import CHECK_INTERVAL
from app.logger import setup_logging
from app.main import check_matches


setup_logging()


def startup_checks():
    """
    Perform startup validation before the scheduler begins.
    """

    logging.info("=" * 50)
    logging.info("FIFA Discord Notifier")
    logging.info("=" * 50)

    logging.info("✓ Logging initialized")
    logging.info("✓ Scheduler interval: %d minutes", CHECK_INTERVAL)

    logging.info("Starting initial match check...")


def job():
    try:
        check_matches()
    except Exception:
        logging.exception(
            "Unexpected error while checking matches."
        )


def run():
    startup_checks()

    # Run immediately
    job()

    logging.info(
        "Scheduler started. Next check every %d minutes.",
        CHECK_INTERVAL,
    )

    schedule.every(CHECK_INTERVAL).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    run()