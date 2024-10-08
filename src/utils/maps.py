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

GENRE_MAP = {
    "allmusicianswelcometojam": "jam session",
    "contemporaryjazz": "jazz",
    "contemporarypop": "pop",
    "easylisteningjazz": "jazz",
    "folk&rock": "folk rock",
    "hiphop": "hip-hop",
    "partypop": "pop",
    "r'n'b": "r&b",
    "rnb": "r&b",
    "r&b": "r&b",
    "summerpop": "pop",
}

NOT_GENRES = [
    "japan",
    "日本",
    "china",
    "中國",
    "re'call",
    "羊文學",
    "行動派",
    "張蔓姿",
    "lagchun",
]

VENUE_MAP = {
    "28restaurant": "28 Restaurant",
    "aftermath": "The Aftermath",
    "alluremusic": "Allure Music Salon",
    "aqualand": "Aqualand",
    "cccpopupspace": "cccpopupspace",
    "champagnebarlobbygrandhyatt": "Grand Hyatt Champagne Bar",
    "cheektocheeksoho": "Cheek to Cheek Soho",
    "cheztrente": "Chez Trente",
    "dalecandela": "Dale Candela",
    "diesel": "Diesel's",
    "dragonfly": "Dragonfly",
    "ella26": "ELLA",
    "fairviewmansion": "Fairview Mansion",
    "fountaindechopin": "Fountain de Chopin",
    "foxglove": "Foxglove",
    "freespacethebox": "Freespace The Box",
    "fringedairy": "Fringe Dairy",
    "hollybrown": "Holly Brown Coffee Roasters",
    "hongkongculturalcentre": "Hong Kong Cultural Centre",
    "hongkongculturalcenter": "Hong Kong Cultural Centre",
    "ironfairies": "Iron Fairies",
    "kindofbrew": "Kind of Brew",
    "laubakfreespace": "Lau Bak Freespace Livehouse",
    "loststars": "Lost Stars Livehouse",
    "lumosrestaurant": "LUMOS Restaurant and Bar",
    "maggiechoo": "Maggie Choo's",
    "momlivehouse": "MOM Live House",
    "ohmcafe": "Ohm… cafe and bar",
    "ohm…": "Ohm… cafe and bar",
    "oneness": "Oneness",
    "paksharoad": "Pak Sha Road",
    "pizzaexpressshopg31": "Pizza Express, Empire Centre",
    "ploungebyplaisance": "P Lounge by Plaisance",
    "ritatongliu": "Rita Tong Liu Drama Theatre",
    "shop222a": "Lost Stars Livehouse",
    "shuntakexhibition": "Shun Tak Exhibition & Event Space",
    "sohohouse": "Soho House",
    "terriblebaby": "Terrible Baby",
    "thesanctum": "The Sanctum",
    "thesouthside": "The Southside",
    "thestage": "The Stage",
    "threesheets": "Three Sheets Marquee Bar",
    "urbansky": "Urban Sky",
    "wanch": "The Wanch",
    "y-theatre": "Y-Theatre"
}

ADDRESS_MAP = {
    "28 Restaurant": ["28 Yi Chun St, Sai Kung", "西貢宜春街28號"],
    "Allure Music Salon": ["3 School St, Tai Hang, Causeway Bay", "銅鑼灣大坑書館街3號"],
    "Aqualand": ["Water World Ocean Park Hong Kong, 33 Ocean Drive, Aberdeen", "香港香港仔海洋徑33號 香港海洋公園水上樂園"],
    "cccpopupspace": ["G/F, 23 New Market St, Sheung Wan", "上環新街市街23號地舖"],
    "Cheek to Cheek Soho": ["17 Old Bailey St, Central", "中環奧卑利街17號"],
    "Chez Trente": ["39 Staunton St, Central", "中環士丹頓街39號"],
    "Dale Candela": ["23 Main St, Yung Shue Wan, Lamma Island", "南丫島榕樹灣大街23號"],
    "Diesel's": ["51 Main St, Yung Shue Wan, Lamma Island", "南丫島榕樹灣大街51號地下"],
    "Dragonfly": ["Shop 10-G1, Tai Kwun, Hollywood Rd, Central", "中環荷李活道10號 大館10-G1舖"],
    "ELLA": ["26/F, The Trilogy, H Code, 45 Pottinger St, Central", "中環砵甸乍街45號 H Code 26樓"],
    "Fairview Mansion": ["Shop A&C, G/F, Fairview Mansion, 51 Paterson St, Causeway Bay", "銅鑼灣百德新街51號華爾大廈 A&C地舖"],
    "Fountain de Chopin": ["6/F, Block B, Kai Tak Factory Building, Stage 1, 22 Sam Chuk St, San Po Kong", "新蒲崗三祝街22號啟德工業大廈第一期B座六樓 翻騰三周半"],
    "Foxglove": ["2/F Printing House, 6 Duddell St, Central", "中環都爹利街6號印刷行2樓"],
    "Freespace The Box": ["Freespace The Box, West Kowloon", "西九文化區自由空間大盒"],
    "Fringe Dairy": ["Fringe Club, 2 Lower Albert Rd, Central", "中環下亞厘畢道二號藝穗會賽奶庫"],
    "Grand Hyatt Champagne Bar": ["Grand Hyatt Hong Kong 1 Harbour Road, Wan Chai", "香檳吧,香港君悅酒店,灣仔港灣道1號"],
    "Holly Brown Coffee Roasters": ["G01, G/F, D2 Place Two, 15 Cheung Shun St, Lai Chi Kok", "九龍荔枝角長順街15號 D2第二期地下G01號舖"],
    "Hong Kong Cultural Centre": ["Hong Kong Cultural Centre", "香港文化中心"],
    "Iron Fairies": ["1-13 Hollywood Rd, Central", "中環荷李活道1-13號"],
    "Lost Stars Livehouse": ["Shop 222A, Level 2, K11 Art Mall, 18 Hanoi Rd, Tsim Sha Tsui", "尖沙咀 河內道18號K11 購物藝術館 2樓222A號"],
    "Kind of Brew": ["G/F, 112 First St, Sai Ying Pun", "西營盤第一街112號地下"],
    "Lau Bak Freespace Livehouse": ["G/F, Freespace, West Kowloon Cultural District, 18 Museum Drive, Tsim Sha Tsui", "尖沙咀西九文化區自由空間地舖 留白 Livehouse"],
    "LUMOS Restaurant and Bar": ["Shop 13-14, G/F Lakeshore Building, 7 Tseng Choi St, Tuen Mun", "屯門井財街7號力生大廈地下13-14號舖"],
    "Maggie Choo's": ["G/F Chinachem Hollywood Centre, Central", "中環華懋荷李活中心"],
    "MOM Live House": ["Shop B38, Seven Seas Shopping Centre, 117-121 Kings Rd, North Point", "北角英皇道117-121號 七海商業中心 店鋪B38"],
    "Ohm… cafe and bar": ["152 Yu Chau St, Sham Shui Po", "深水埗汝州街152號"],
    "Oneness": ["Rm 11 9/F, Wing Hing Industrial Building, 14 Hing Yip St, Kwun Tong, Kowloon", "觀塘興業街14號永興工業大廈9樓C11室太一"],
    "P Lounge by Plaisance": ["G/F, 1 Duddell St, Central", "中環都爹利街1號地舖"],
    "Pak Sha Road": ["Pak Sha Rd, Causeway Bay", "銅鑼灣白沙道"],
    "Pizza Express, Empire Centre": ["Shop G31-33, 49-51 Empire Centre, 68 Mody Rd, Tsim Sha Tsui", "尖沙咀麼地道68號帝國中心地下G31-33及G49-51號舖"],
    "Rita Tong Liu Drama Theatre": ["1 Gloucester Rd, Wan Chai", "灣仔告士打道一號廖湯惠靄戲劇院"],
    "Shun Tak Exhibition & Event Space": ["4/F, Shun Tak Centre, 200 Connaught Rd Central", "香港上環干諾道中200號信德中心4樓信德展覽及活動空間"],
    "Soho House": ["33 Des Voeux Rd West, Sheung Wan", "上環德輔道西33號"],
    "Terrible Baby": ["4/F, Easton HK, 380 Nathan Rd, Kowloon", "九龍彌敦道380號"],
    "The Aftermath": ["L/G, 57-59 Wyndham St, Central", "中環雲咸街57-59號低層地下"],
    "The Sanctum": ["3/F, Stanley 11, 11 Stanley St, Central", "中環士丹利街11號Stanley 11 3樓"],
    "The Southside": ["LG Atrium, 11 Heung Yip Rd, Wong Chuk Hang", "黃竹坑香葉道11號LG中庭"],
    "The Stage": ["2/F, The Heritage Woo Cheong Pawn Shop, 60A-66 Johnston Rd, Wan Chai", "灣仔莊士敦道62號 2樓"],
    "The Wanch": ["1/F, Henan Building, 90 Jaffe Rd, Wan Chai", "灣仔謝斐道90號豫港大廈1樓"],
    "Three Sheets Marquee Bar": ["Shop G06, G/F, D'Deck, 8-12 Plaza Lane, Discovery Bay", "愉景灣廣場徑8-12號D'Deck地下G06號舖"],
    "Urban Sky": ["9/F, Hysan Place", "希慎廣場9樓"],
    "Y-Theatre": ["LG1, Youth Square, 238 Chai Wan Rd", "香港柴灣道238號青年廣場LG1 Y-Theatre"]
}

