import json
from pathlib import Path

FILE = Path("sent_matches.json")


def load_sent():

    if not FILE.exists():
        return set()

    with open(FILE, "r") as f:
        return set(json.load(f))


def save_sent(sent):

    with open(FILE, "w") as f:
        json.dump(list(sent), f, indent=4)