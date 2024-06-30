DAY_MAP = {
    "monday": 1,
    "tuesday": 2,
    "wednesday": 3,
    "thursday": 4,
    "friday": 5,
    "saturday": 6,
    "sunday": 7,
}

TIER_MAP = {
    # Strip out spaces and hypens to ease comparisons
    "1dayticket一日票": "1_day",
    "2dayticket二日票": "2_day",
    "2dayticket兩日票": "2_day",
    "3dayticket三日票": "3_day",
    "advance預售": "advance",
    "afterparty": "after_party",
    "door即場": "door",
    "earlybird早鳥": "advance",
    "fringeclubmember藝穗會會員": "member",
    "fulltimestudent全日制學生": "student",
    "monthlypass月票": "monthly_pass",
    "regular正價": "standard",
    "student學生": "student",
    "vip": "vip",
    "walkin即場": "door",
}

GENRE_MAP = {"r'n'b": "r&b", "rnb": "r&b", "r&b": "r&b"}

LOCATION_LIST = ["Japan", "日本", "China", "中國"]
