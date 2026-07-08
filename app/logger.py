import logging
from pathlib import Path


def setup_logging():
    """
    Configure application-wide logging.

    Logs are written to both the console and
    logs/notifier.log.
    """

    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / "notifier.log"

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    logger = logging.getLogger()

    # Prevent duplicate handlers if setup_logging()
    # is called more than once.
    if logger.handlers:
        return

    logger.setLevel(logging.INFO)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)