"""
Contains the scraping fuctions for the basic craiglist scraper
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from urllib.parse import quote_plus
import time
from scraper_functs.config import DELAY

# query ,max_results
def get_cutoff_time():
    """Gets the the UTC of yesterday at 7:00 p.m."""
    now_et = datetime.now(ZoneInfo("America/New_York"))

    cutoff_et = (now_et - timedelta(days=1)).replace(hour=19, minute=0, second=0, microsecond=0)

    cutoff_utc = cutoff_et.astimezone(ZoneInfo("UTC"))

    return cutoff_utc


def scrap_all_results(url, known_ids, recent: bool, zone: int):
    """
    Scrape a maximum number of results for a given url that are under 24 hours old if recent is true
    Skips known urls based on post id
    zone is for the area zone the listing is in
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    # first scrape all results from the page
    print(f"Scraping query page: {url}")
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')

    with open("craigslist_page.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())

    listings = soup.find_all("li", class_="cl-static-search-result")
    max_listings = len(listings)
    print(response)
    print(f"Found {max_listings} listings")

    # start scraping each page starting at the first one (newest first)
    # once a result that has been posted more than 24 hours ago from 7.p.m. has been scraped, stop
    results = []
    time_cutoff = get_cutoff_time()

    for li in listings:
        # make sure it is a normal url
        a_tag = li.find("a")
        if not a_tag:
            continue

        li_url = a_tag["href"]
        post_id = li.get("data-pid") or li_url.split("/")[-1].split(".")[0]

        if post_id in known_ids:
            print(f"ID already known, skipping: {li_url} \n")
            continue

        # Scrape the individual page for more info
        print(f"Scraping individual page: {li_url}")
        print(f"Requesting at {datetime.now().isoformat()}")
        li_response = requests.get(li_url, headers=headers)
        li_soup = BeautifulSoup(li_response.content, 'html.parser')

        # with open("craigslist_page.html", "w", encoding="utf-8") as f:
            # f.write(li_soup.prettify())

        # Extract posting datetime
        time_tags = li_soup.find_all("time", {"class": "date timeago"})

        post_time_utc = None
        update_time_utc = None

        if len(time_tags) >= 2:
            try:
                post_time = datetime.strptime(time_tags[1]["datetime"], "%Y-%m-%dT%H:%M:%S%z")
                post_time_utc = post_time.astimezone(ZoneInfo("UTC"))
            except Exception as e:
                print(f"Error parsing post time: {e}")

        if len(time_tags) >= 3:
            try:
                update_time = datetime.strptime(time_tags[2]["datetime"], "%Y-%m-%dT%H:%M:%S%z")
                update_time_utc = update_time.astimezone(ZoneInfo("UTC"))
            except Exception as e:
                print(f"Error parsing update time: {e}")
        else:
            # if no update time, should break loop if post time is old
            update_time_utc = post_time_utc

        # if recent skip all old posts
        if recent:
            # Skip old posts
            print(f"post time: {post_time_utc}")
            print(f"update time time: {update_time_utc}")
            print(f"time_cutoff: {time_cutoff}")
            
            # break if update time is old, as it means every update and post time after is also old
            if update_time_utc < time_cutoff:
                print("Update time is older than 24 hours, stopping early.")
                print("")
                break
            
            # only skip if post time is old, as its update time can make it appear high in the order
            if post_time_utc < time_cutoff:
                print("Post time is older than 24 hours, skipping \n")
                continue

        # get all relavent info and add listing to results
        title_tag = li_soup.find("span", id="titletextonly")
        price_tag = li_soup.find("span", class_="price")
        location_tag = li_soup.find("small")
        desc_tag = li_soup.find("section", id="postingbody")

        title = title_tag.text.strip() if title_tag else ""
        price = price_tag.text.strip() if price_tag else ""
        location = location_tag.text.strip(" ()") if location_tag else ""
        description = (
            desc_tag.get_text(separator="\n", strip=True).replace("QR Code Link to This Post", "")
            if desc_tag else ""
        )

        # add to results
        results.append({
            "post_id": post_id,
            "url": li_url,
            "title": title,
            "price": price,
            "location": location,
            "description": description,
            "post_time": post_time.isoformat(),
            "zone": zone
        })

        known_ids.add(post_id)
        time.sleep(DELAY)
        print(f"Done sleeping at {datetime.now().isoformat()}\n")

    # return all results 
    return results


def get_relevant_items(queries: list[str], locations: list[tuple[str, float, float, float, int]], known_ids: list[str], recent: bool):
    """
    Returns items under 24 hours old for all queries at all locations if recent is true
    otherwise get all items in the first page of relavent results for all queries for all locations
    """
    all_results = []
    # loop over each query for each location
    # must build each url from locations and queries
    for region, lat, lon, radius, zone in locations:
        for query in queries:
            base_url = f"https://{region}.craigslist.org/search/sss"
            if recent:
                params = f"?query={quote_plus(query)}&lat={lat}&lon={lon}&search_distance={radius}&sort=date"
            else:
                params = f"?query={quote_plus(query)}&lat={lat}&lon={lon}&search_distance={radius}&sort=rel"
            url = base_url + params
            results = scrap_all_results(url, known_ids, recent, zone)
            all_results.extend(results)
            time.sleep(DELAY)

    return all_results