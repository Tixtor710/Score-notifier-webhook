import logging
import time

import schedule

from app.config import CHECK_INTERVAL
from app.logger import setup_logging
from app.main import check_matches


setup_logging()


def job():
    try:
        check_matches()
    except Exception:
        logging.exception(
            "Unexpected error while checking matches."
        )


logging.info("===================================")
logging.info("FIFA Discord Notifier Started")
logging.info(
    "Checking every %d minutes...",
    CHECK_INTERVAL,
)
logging.info("===================================")

job()

schedule.every(CHECK_INTERVAL).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)