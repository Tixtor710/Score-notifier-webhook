import logging

import requests

from app.config import FIFA_ENDPOINT


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) "
        "Gecko/20100101 Firefox/140.0"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://www.fifa.com",
    "Referer": "https://www.fifa.com/",
    "Connection": "keep-alive",
}


def get_matches():
    """Fetch all World Cup matches from the FIFA API."""

    try:
        response = requests.get(
            FIFA_ENDPOINT,
            headers=HEADERS,
            timeout=20,
        )

        response.raise_for_status()

        logging.info(
            "Successfully retrieved data from FIFA API."
        )

        return response.json()

    except requests.exceptions.Timeout:
        logging.exception(
            "FIFA API request timed out."
        )
        raise

    except requests.exceptions.HTTPError:
        logging.exception(
            "FIFA API returned %s\n%s",
            response.status_code,
            response.text,
        )
        raise

    except requests.exceptions.RequestException:
        logging.exception(
            "Unable to reach FIFA API."
        )
        raise

    except ValueError:
        logging.exception(
            "FIFA API returned invalid JSON."
        )
        raise