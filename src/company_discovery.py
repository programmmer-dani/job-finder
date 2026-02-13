import json
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from pathlib import Path

geolocator = Nominatim(user_agent="job-finder ([PROJECT_LINK])")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1, max_retries=2)
# IN: get city name & types of companies
# OUT: companies names and websites


def find_companies(cities, company_tags):
    cache_path = Path("data/city_cache.json")
    cache_exists = cache_path.exists()
    cache = {}

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
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2)
    else:
        # TODO: Notify no cities found
        return {}

    for tag in company_tags:
        # create query
        # activate API
        continue


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
