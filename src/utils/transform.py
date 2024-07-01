import os
import re
import sys

sys.path.append(os.path.join(os.path.dirname(__file__)))
from maps import DAY_MAP, GENRE_MAP, NOT_GENRES, TIER_MAP


def convert_days_to_digits(day_string) -> int:
    """
    Converts weekday names to digit equivalent
    Monday -> 1
    """
    return DAY_MAP[day_string.lower()]


def convert_to_24_hour_time(time_str: str) -> str:
    """
    Converts analogue time to 24-hour time
    7pm -> 19:00
    4:15am -> 04:15
    late -> 00:00

    Parameters
    ----------
    time_str : str
        original time string

    Returns
    -------
    time_str in 24-hour format
    """
    if time_str is None:
        return "??:??"

    match = re.match(r"(\d{1,2}):?(\d{2})?\s*(a\s?m|p\s?m)", time_str.lower())

    if not match:  # "late" rarely appears so don't check by default
        if time_str.lower() == "late":
            return "00:00"
        # Return original string if it doesn't match the pattern
        return time_str

    hour, minute, period = match.groups()
    hour = int(hour)

    if ("pm" in period or "p m" in period) and hour != 12:
        hour += 12
    elif ("am" in period or "a m" in period) and hour == 12:
        hour = 0

    if minute:
        return f"{hour:02}:{minute:02}"

    return f"{hour:02}:00"


def match_ticket_tiers(price_string: str) -> tuple:
    """
    Applies regex to determine price and category
    for a string with a single price & optional tier

    Parameters
    ----------
    price_string : str
        string including single price and optional tier info

    Returns
    -------
    _ : str
        tier description

    _ : int
        price
    """
    pattern = re.compile(
        r"""
        (?:HK)?   # optional HK prefix
        \$?       # optional "$" sign prefix
        (\d+)     # numbers to capture
        [\s]*     # optional whitespace
        \(?       # optional "(" sign
        ([^\)]*)  # tier description to capture
        \)?       # optional ")" sign
        """,
        re.VERBOSE | re.DOTALL,
    )
    # Get matches
    matches = pattern.findall(price_string)
    if matches:
        if matches[0][1] == "":
            # Interpret blank tier descriptions as "standard"
            return "standard", int(matches[0][0])
        # Remove spaces to avoid whitespace typos
        spaceless_match = matches[0][1].replace(" ", "").replace("-", "").lower()
        if spaceless_match in TIER_MAP:
            # Get tier description from TIER_MAP
            return TIER_MAP[spaceless_match], int(matches[0][0])

        # Return tier description as-is if not in TIER_MAP
        return matches[0][1], int(matches[0][0])


def convert_ticket_prices(prices: str) -> dict:
    """
    Converts ticket prices into standard format

    Parameters
    ----------
    prices : str
        string containing one or more prices & price tier descriptions

    Returns
    -------
    ticket_prices : dict
        map of tier descriptions to ticket prices
        for a given event
    """
    if "free entry" in prices.lower() or "免費入場" in prices:
        return {"standard": 0}

    ticket_prices = dict()
    tiers = [price.strip() for price in prices.split(",")]

    for t in tiers:
        tier, price = match_ticket_tiers(t)
        ticket_prices[tier] = price

    return ticket_prices


def split_genres(genres: str) -> list[str]:
    """
    Creates a list of genres from a string

    Parameters
    ----------
    genres : str
        genres associated with a band

    Returns
    -------
    list[str]
        genres separated into list elements
    """
    # Ignore place names and band names
    if any(loc in genres.lower() for loc in NOT_GENRES):
        return None
    # Ignore strings with phone numbers
    if re.match(r".*([\d]{4}[-\s]?[\d]{4}).*", genres):
        return None

    # Split genres by commas and slashes
    parts = re.split(r"[,/]", genres)

    genre_list = list()
    for part in parts:
        # Add to list but split
        genre_list.extend(part.split(" & "))

    # Strip whitespace and make all entries lowercase
    genre_list = [genre.lower().strip() for genre in genre_list]

    return [
        # Remove inner whitespace and hypens to compare with GENRE_MAP
        GENRE_MAP[genre.replace(" ", "").replace("-", "")]
        if genre.replace(" ", "").replace("-", "") in GENRE_MAP
        else genre
        for genre in genre_list
    ]


def parse_genres(genre_string: str) -> list[str]:
    """
    Applies regex to find genre info in a string

    Parameters
    ----------
    genre_string : str
        band and genre string to parse

    Returns
    -------
    genre_list : list[str]
        sorted list of genres found
    """
    # Grab text between "()" signs
    pattern = re.compile(r"\(([^\)]+)\)?")
    # May be 0 or multiple matches
    matches = pattern.findall(genre_string)
    if matches:
        genre_list = list()
        for match in matches:
            genres = split_genres(match)
            if genres is not None:
                genre_list.extend(genres)

        if genre_list and len(genre_list) > 1:
            return sorted(list(set(genre_list)))
        return genre_list

    return ["unknown"]


def parse_band_name(band_string: str) -> str:
    """
    Extracts a band name from a string

    Parameters
    ----------
    band_string : str
        band with genre info

    Returns
    -------
    band : str
        band name
    """
    # Grab text until a "(" sign
    pattern = re.compile(r"([^\(]+)\s*\(?")
    # Get band name
    match = pattern.search(band_string.strip())
    if match:
        band = match.group(1).strip()
        return band

    return "unknown"


def parse_all_bands_and_genres(bands_string: str) -> list[dict]:
    """
    Extracts band and genre info into a list
    with a dict for each band's name and declared genres

    Parameters
    ----------
    bands_string : str
        bands and genres from event content

    Returns
    -------
    new_bands_list : list[dict]
        list of dict for each band
        containing name and genre details
    """
    bands_list = bands_string.split("),")
    new_bands_list = list()

    for band in bands_list:
        band = band.strip()
        band_name = parse_band_name(band)
        band_genre = parse_genres(band)
        new_bands_list.append({"name": band_name, "genre": band_genre})

    return new_bands_list


def format_matches(matches: list[re.Match]) -> list[dict]:
    """
    Applies standard format to matched entities

    Parameters
    ----------
    matches : list[re.Match]
        list of entries extracted via regex

    Returns
    -------
    instance_list : list[dict]
        list of matches formatted into dict objects
    """
    # List to store instances
    instance_list = list()
    # Add matches to list
    for match in matches:
        # Create dict object
        event = {
            key: (value.strip() if value is not None else None)  # handle missing values
            for key, value in match.groupdict().items()
        }
        # Convert weekday names to digits
        event["weekday"] = convert_days_to_digits(event["weekday"])
        # Convert month and date strings to int
        event["month"] = int(event["month"])
        event["date"] = int(event["date"])

        if event["desc"] == "":
            # Add description if missing
            event["desc"] = "Unknown"

        # Convert times to 24-hour strings
        event["open"] = convert_to_24_hour_time(event["open"])
        event["close"] = convert_to_24_hour_time(event["close"])

        # Get list of bands and their genres
        event["bands"] = parse_all_bands_and_genres(event["bands"])

        # Parse ticket prices by tier
        event["tickets"] = convert_ticket_prices(event["tickets"])
        # Add event to instance list
        instance_list.append(event)

    return instance_list
