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
    match = re.match(r"(\d{1,2}):?(\d{2})?(am|pm)", 
        time_str.lower())
    
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


# def convert_ticket_prices(prices: str) -> dict:
#     """
#     """
#     if prices == "Free Entry 免費入場":
#         return 0.0


def format_matches(matches: list[re.Match]) -> list[dict]:
    """ """
    # List to store instances
    instance_list = list()
    # Add matches to list
    for match in matches:
        # Create dict object
        event = {key: value.strip() for key, value in match.groupdict().items()}
        # Convert weekday names to digits
        event["weekday"] = convert_days_to_digits(event["weekday"])
        # Convert times to 24-hour strings
        event["open"] = convert_to_24_hour_time(event["open"])
        event["close"] = convert_to_24_hour_time(event["close"])
        # Add event to instance list
        instance_list.append(event)
        print(event)

    return instance_list
