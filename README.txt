Overview:
	This project is a python based automaton tool that scrapes Craigslist listings based on configurable search queries and locations,
	filters them for relevance, and sends a structured email summary of the results. Currently configured to run on a AWS E2C instance.
	It is designed to reduce manual searching by automatically identifying new listings and delivering them in a clean, readable format.

Key Features:
	Automated Web Scraping: The program scrapes Craigslist using requests and BeautifulSoup, and it supports multiple search queries and geographic regions
	Time-Based Filtering: Option to retrieve only listings from the past 24 accuracy, and it uses timezone-aware datetime handling for accuracy
	Custom Relevance Filtering: Filters listings based on required and excluded phrases, which improves signal-to-noise ratio of results
	Email Notification System: Sends formatted email summaries (plain text + HTML), then groups listings by proximity zones
	Command-Line Interface: Supports runtime configuration via CLI arguments. Example: python -m scraper recent --email-test

Example Workflow
	User defines their search queries and location needs
	Input that data into the config
	Program scrapes listings from Craigslist
	Filter results based on relevance criteria
	Sends an email with matching listings

Technologies Used
	Python
	requests(HTTP requests)
	beautifulSoup(HTML Parsing)
	smtplib(email sending)
	argparse(CLI)

Project Structure
project/
	__main__.py # Entry point (CLI + orchestration) 
	scraper.py # Scraping logic 
	filter.py # Filtering logic 
	email_sender.py # Email construction and delivery 
	config.py # Configuration (queries, locations, credentials)

Engineering Highlights
	Modular pipeline architecture(scraping -> filtering -> notification)
	Incorporates rate limiting to avoid server overload

Notes
	Email sending uses Gmail SMTP with SSL
	app passwords are required for authentication
	currently configured to store sensitive data (email addresses and passwords) in the local environment in .env
