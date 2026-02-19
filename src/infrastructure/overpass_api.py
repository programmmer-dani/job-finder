import requests


def fetch_api_result(query):
    url = "https://overpass-api.de/api/interpreter"
    try:
        response = requests.post(url, data={"data": query}, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        pass
    return None