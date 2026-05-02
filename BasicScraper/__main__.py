import argparse
import scraper_functs
from scraper_functs.config import SENDER_EMAIL, RECEIVER_EMAIL, APP_PASSWORD, QUERIES, LOCATIONS, PORT, REMOVEPHRASES



def main():
    # keep all known urls
    known_ids = set()

    # get command line arguments(i.e. recency and if gmail test)
    parser = argparse.ArgumentParser(description="Send email with listings.")
    
    # Positional argument: "recent" (default) or "all"
    parser.add_argument(
        "mode",
        choices=["recent", "all"],
        nargs="?",
        default="recent",
        help="Choose to fetch 'recent'(within 24 hours) listings (default) or 'all' listings"
    )

    # Optional flag for test mode
    parser.add_argument(
        "--email-test",
        action="store_true",
        help="Run in test mode (email is printed instead of sent)"
    )

    args = parser.parse_args()
    recent = args.mode == "recent"
    email_test = args.email_test

    # gets all relavent items for all queries at all locations
    # pass in how recent the results should be
    all_results = scraper_functs.get_relevant_items(QUERIES, LOCATIONS, known_ids, recent)

    if not all_results:
        print("No results found.")
        # return

    print(f"\n Found {len(all_results)} new listings:\n")
    for result in all_results:
        print(f"Title: {result.get('title')}")
        print(f"Post ID: {result.get('post_id')}")
        print(f"Location: {result.get('location')}")
        print(f"Post Time: {result.get('post_time')}")
        print(f"URL: {result.get('url')}")
        print("")

    # do some additional filtering based on some criteria
    # might be a little crude, but use the same search queries as the filter phrases
    filtered_results = scraper_functs.filter_results(all_results, QUERIES, REMOVEPHRASES)

    # filtered_results = all_results # for testing, so it has some output of some kind

    print(f"\n Found {len(filtered_results)} Filtered listings:\n")
    for result in filtered_results:
        print(f"Title: {result.get('title')}")
        print(f"Post ID: {result.get('post_id')}")
        print(f"Location: {result.get('location')}")
        print(f"Post Time: {result.get('post_time')}")
        print(f"URL: {result.get('url')}")
        print("")

    # send email with results
    scraper_functs.send_emails(PORT, SENDER_EMAIL, RECEIVER_EMAIL, APP_PASSWORD, filtered_results, email_test)

if __name__ == "__main__":
    main()