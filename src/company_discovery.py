import json
import time
import requests
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from pathlib import Path

geolocator = Nominatim(user_agent="job-finder ([PROJECT_LINK])")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1, max_retries=2)

# IN: get city name & types of companies
# OUT: companies names and websites
def find_companies(cities, company_tags=["it"]):
    cache_path = Path("data/city_cache.json")
    cache_exists = cache_path.exists()
    cache = {}
    api_results = []

    # load cache (if exists)
    if cache_exists:
        cache = load_cache(cache_path)

    for city in cities:
        key = f"{city.strip().lower()}"
        if key in cache:
            value = cache[key]
        else:
            value = fetch_city_values(key)
            if value is not None:
                cache[key] = value
            else:
                # TODO: Notify not found city
                continue

    if cache != {}:
        save_cache(cache, cache_path)
    else:
        # TODO: Notify no cities found
        return {}
    
    # Create list of all queries
    queries = compose_queries(cache, company_tags)

    # Call API for each query
    for query in queries:
        raw_result = fetch_api_result(query)
        if raw_result is not None:
            results = format_api_result(raw_result)
            api_results.append(results)
        time.sleep(1)


def format_api_result(result):
    if result is not None and "elements" in result:
        return result["elements"]
    return []

def fetch_api_result(query):
    url = "https://overpass-api.de/api/interpreter"
    try:
        response = requests.post(url, data={"data": query}, timeout=30)
        response.raise_for_status()
        formatted_response = response.json()
        return formatted_response
    except requests.RequestException:
        # TODO: Notify API error
        pass
    return None
    
def compose_queries(cache, office_tags):
    queries = []
    for key, value in cache.items():
        bbox = value.get("bbox")
        if not bbox or len(bbox) < 4:
            continue
        south, north, west, east = float(bbox[0]), float(bbox[1]), float(bbox[2]), float(bbox[3])
        for tag in office_tags:
            q = f'[out:json][timeout:25];\nnode["office"="{tag}"]["website"]({south},{west},{north},{east});\nout body;'
            queries.append(q)
    return queries
            
    

def fetch_city_values(key):
    location = geocode(key, exactly_one=True)
    if location is not None:
        value = {
            "lat": location.latitude,
            "lon": location.longitude,
            "bbox": location.raw["boundingbox"],
        }
        return value
    return None


def load_cache(cache_path):
    try:
        with open(cache_path, "r", encoding="utf-8") as f:
            cache = json.load(f)
        return cache
    except json.JSONDecodeError:
        return {}
    
def save_cache(cache, cache_path):
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)


"""
# Hardcoded office tag for use case of:
# finding software development internships,
# future improvement: Make this a parameter corresponding the users usecase for this program
OFFICE_TAGS = ["it"]
"""