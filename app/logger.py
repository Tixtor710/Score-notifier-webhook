import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging():
    """
    Configure application-wide logging.

    Logs are written to both the console and
    logs/notifier.log.

    The log file automatically rotates when it
    reaches 5 MB.
    """

    logger = logging.getLogger()

    # Prevent duplicate handlers
    if logger.handlers:
        return

    logger.setLevel(logging.INFO)

    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        log_dir / "notifier.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)