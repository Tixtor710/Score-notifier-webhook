import os
from dotenv import load_dotenv

load_dotenv()


def require_env(name: str) -> str:
    """
    Return an environment variable or raise an error if it is missing.
    """

    value = os.getenv(name)

    if value is None:
        raise RuntimeError(
            f"Missing required environment variable: {name}"
        )

    value = value.strip()

    if value == "":
        raise RuntimeError(
            f"Environment variable '{name}' is empty."
        )

    return value


DISCORD_WEBHOOK = require_env("DISCORD_WEBHOOK")
FIFA_ENDPOINT = require_env("FIFA_ENDPOINT")

NOTIFICATION_WINDOW = int(
    os.getenv("NOTIFICATION_WINDOW", "30")
)

CHECK_INTERVAL = int(
    os.getenv("CHECK_INTERVAL", "5")
)

# Debug output (temporary)
print("Loaded FIFA endpoint:")
print(repr(FIFA_ENDPOINT))