from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

geolocator = Nominatim(user_agent="job-finder (https://github.com/programmmer-dani)")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1, max_retries=2)


def fetch_city_values(key):
    location = geocode(key, exactly_one=True)
    if location is not None:
        return {
            "lat": location.latitude,
            "lon": location.longitude,
            "bbox": location.raw["boundingbox"],
        }
    return None
