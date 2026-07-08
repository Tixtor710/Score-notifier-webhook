import requests
from config import FIFA_ENDPOINT


HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}


def get_matches():
    response = requests.get(
        FIFA_ENDPOINT,
        headers=HEADERS,
        timeout=20
    )

    response.raise_for_status()

    return response.json()