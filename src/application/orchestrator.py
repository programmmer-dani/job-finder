import os
import certifi

# Certifi so HTTPS works on macOS (avoiding SSL errors). Must run before any request/geopy import.
os.environ.setdefault("SSL_CERT_FILE", certifi.where())
os.environ.setdefault("REQUESTS_CA_BUNDLE", certifi.where())

from domain.company_prioritiser import sort_companies
from presentation.cli import get_user_input, show_results
from domain.company_discovery import find_companies
from infrastructure.scraper import find_career_pages
from infrastructure.html_extractor import fetch_html
from domain.job_matcher import search_matching_position

def run():
    user_input = get_user_input()
    cities = user_input[0]
    keywords = user_input[1]
    company_tags = user_input[2]
    
    companies = find_companies(cities, company_tags)
    
    companies = find_career_pages(companies)
    
    for company in companies:
        company["potential_match"] = False
        if company["career_page"] != "":
            html = fetch_html(company["career_page"])
            if html != "" and search_matching_position(html, keywords):
                company["potential_match"] = True
    
    companies = sort_companies(companies)
    
    show_results(companies)
    
    exit(0)