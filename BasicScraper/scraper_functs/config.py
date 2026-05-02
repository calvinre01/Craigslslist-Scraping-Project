"""
Config File for scraper
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Email settings
PORT = 465
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")


QUERIES = [
    "sunglasses lot",
    "eyewear lot",
    "sunglasses lot",
    "glasses lot",
    "lots of eyeglasses",
    "lots of glasses",
    "lots of sunglasses",
    "lots of eyewear",
    "bulk eyeglasses",
    "bulk glasses",
    "bulk sunglasses",
    "bulk eyewear",
    "lot of eyeglasses",
    "lot of glasses",
    "lot of sunglasses",
    "lot of eyewear"
]
"""
# test query
QUERIES = [
    "glasses lot"
]
"""

# phrases to remove, for the 2nd filter:
REMOVEPHRASES = [
    "wine glass",
    "wine glasses",
    "drinking glass",
    "drinking glasses",
    "water glass",
    "water glasses",
    "whisky glass",
    "whisky glasses",
    "coke glass",
    "coke glasses",
    "coca-cola glass",
    "coca-cola glasses",
    "coca cola glass",
    "coca cola glasses",
    "lismore glass",
    "lismore glasses",
    "pitcher",
    "lions glass",
    "lions glasses",
    "shot glass",
    "shot glasses",
    "pint glass",
    "pint glasses",
    "beer glass",
    "beer glasses",
    "brandy glass",
    "brandy glasses",
    "tumbler",
    "highball glass",
    "highball glasses",
    "lowball glass",
    "lowball glasses",
    "juice glass",
    "juice glasses",
    "glass cup",
    "glass tumbler",
    "glassware",
    "mason jar",
    "bell shape glasses",
    "burger king collectable glasses",
    "glass washer"
]

# get all locations and radiai to query from
# organized by region, lat, lon, radius, zone
# new locations with zones, overlap is ok, should be assigned the first zone it appears in


LOCATIONS = [
    ("battlecreek", 42.3017, -85.2429, 120, 1),
    ("windsor", 42.2509, -82.9947, 90, 1),
    ("annarbor", 42.23, -83.6254, 410, 2),
    ("westernmass", 42.3394, -72.5024, 410, 3),
    ("atlanta", 32.9165, -84.2871, 570, 3),
    ("northplatte", 40.0598, -100.8457, 860, 3),
    ("bend", 45.0549, -120.1203, 450, 3),
    ("lasvegas", 37.0902, -117.29, 400, 3)

]
"""
# test locations
LOCATIONS = [
    ("battlecreek", 42.3017, -85.2429, 120, 1),
    ("annarbor", 42.23, -83.6254, 410, 2)
    # ("westernmass", 42.3394, -72.5024, 410, 3)
]

Old locations to search all USA
LOCATIONS = [
    ("stlouis", 38.8550, -89.9480, 580),
    ("hudsonvalley", 41.528, -74.3794, 590),
    ("auburn", 33.0399, -85.2553, 600),
    ("salina", 38.5825, -97.7783, 800),
    ("kpr", 45.4755, -119.1577, 360),
    ("reno", 37.1567, -118.4115, 490)
]
"""
# delay in between all page scrapes
DELAY = 5.0