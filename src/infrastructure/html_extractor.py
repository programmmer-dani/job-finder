import requests
from bs4 import BeautifulSoup

def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.prettify()
    except requests.exceptions.RequestException as e:
        # TODO: log error fetching html
        return ""