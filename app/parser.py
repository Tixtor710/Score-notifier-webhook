from datetime import datetime


def parse_match(match):

    home = match.get("Home")
    away = match.get("Away")
    stadium = match.get("Stadium")

    if home is None or away is None or stadium is None:
        return None

    home_names = home.get("TeamName")
    away_names = away.get("TeamName")

    if not home_names or not away_names:
        return None

    stadium_names = stadium.get("Name")
    city_names = stadium.get("CityName")

    if not stadium_names or not city_names:
        return None

    return {
        "id": match["IdMatch"],
        "home": home_names[0]["Description"],
        "away": away_names[0]["Description"],
        "stadium": stadium_names[0]["Description"],
        "city": city_names[0]["Description"],
        "kickoff": datetime.fromisoformat(
            match["Date"].replace("Z", "+00:00")
        ),
    }