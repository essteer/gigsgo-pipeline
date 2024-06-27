import re


def convert_days_to_digits(day_string) -> int:
    """
    Converts weekday names to digit equivalent
    Monday -> 1
    """
    day_digits = {
        "monday": 1,
        "tuesday": 2,
        "wednesday": 3,
        "thursday": 4,
        "friday": 5,
        "saturday": 6,
        "sunday": 7,
    }

    return day_digits[day_string.lower()]


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
    match = re.match(r"(\d{1,2}):?(\d{2})?(am|pm)", time_str.lower())

    if not match:  # "late" rarely appears so don't check by default
        if time_str.lower() == "late":
            return "00:00"
        # Return original string if it doesn't match the pattern
        return time_str

    hour, minute, period = match.groups()
    hour = int(hour)

    if period == "pm" and hour != 12:
        hour += 12
    elif period == "am" and hour == 12:
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
    tier_map = {
        "1-day ticket 一日票": "1_day",
        "3-day ticket 三日票": "3_day",
        "advance 預售": "advance",
        "after party": "after_party",
        "door 即場": "door",
        "early-bird 早鳥": "advance",
        "fringe club member 藝穗會會員": "member",
        "full time student 全日制學生": "student",
        "monthly pass 月票": "monthly_pass",
        "regular 正價": "standard",
        "student 學生": "student",
        "vip": "vip",
        "walk-in 即場": "door",
    }
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

        if matches[0][1].lower() in tier_map:
            # Get tier description from tier_map
            return tier_map[matches[0][1].lower()], int(matches[0][0])

        # Return tier description as-is if not in tier_map
        print(f"Unknown price tier: {matches[0][1]}")
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
    if prices == "Free Entry 免費入場" or prices == "Free Entry 免費⼊場":
        return {"standard": 0}

    ticket_prices = dict()
    tiers = [price.strip() for price in prices.split(",")]

    for t in tiers:
        tier, price = match_ticket_tiers(t)
        ticket_prices[tier] = price

    return ticket_prices


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
        event = {key: value.strip() for key, value in match.groupdict().items()}
        # Convert weekday names to digits
        event["weekday"] = convert_days_to_digits(event["weekday"])
        # Convert month and date strings to int
        event["month"] = int(event["month"])
        event["date"] = int(event["date"])
        # Convert times to 24-hour strings
        event["open"] = convert_to_24_hour_time(event["open"])
        event["close"] = convert_to_24_hour_time(event["close"])
        # Parse ticket prices by tier
        event["tickets"] = convert_ticket_prices(event["tickets"])
        # Add event to instance list
        instance_list.append(event)

    return instance_list
