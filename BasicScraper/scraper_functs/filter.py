"""
Filter Fuctions for craiglist scraper
"""

def filter_results(all_results: list[dict], phrases: list[str], remove_phrases: list[str]):
    """
    Filters scraped listings to ensure a desgree of quality/accuracy/specificity
    Looks for any of the given phrases in the title and desc of the listing
    """
    print("First filter being applied")
    filtered = []
    filter_2 = []

    lower_phrases_set = set([phrase.lower() for phrase in phrases])
    low_remove_phrases_set = set([phrase.lower() for phrase in remove_phrases])

    for listing in all_results:
        title = listing["title"].lower()
        description = listing["description"].lower()

        if any(phrase in title or phrase in description for phrase in lower_phrases_set):
            filtered.append(listing)

    print("2nd filter being applied")
    for listing in filtered:
        title = listing["title"].lower()
        description = listing["description"].lower()

        if not any(phrase in title or phrase in description for phrase in low_remove_phrases_set ):
            filter_2.append(listing)

    return filter_2