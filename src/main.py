import os
import certifi

# Certifi so HTTPS works on macOS (avoiding SSL errors). Must run before any request/geopy import.
os.environ.setdefault("SSL_CERT_FILE", certifi.where())
os.environ.setdefault("REQUESTS_CA_BUNDLE", certifi.where())

from infrastructure.scraper import find_career_pages
from application.company_discovery import find_companies
from presentation.cli import get_cities

if __name__ == "__main__":
    cities = get_cities()
    companies = find_companies(cities)
    companies = find_career_pages(companies)
