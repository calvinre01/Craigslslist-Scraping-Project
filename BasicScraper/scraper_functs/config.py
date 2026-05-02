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

# the queries to search for on craigslist
# example query "glasses lot"
QUERIES = [
    ""
]

# phrases to remove, for the 2nd filter:
# sample phrase : "wine glass"
REMOVEPHRASES = [
    ""
]

# get all locations and radiai to query from
# organized by region, lat, lon, radius, zone
# new locations with zones, overlap is ok, should be assigned the first zone it appears in
# example: "battlecreek", 42.3017, -85.2429, 120, 1)

LOCATIONS = []

# delay in between all page scrapes
DELAY = 5.0