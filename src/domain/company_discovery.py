from infrastructure.cache_repository import load_cache, save_cache
from infrastructure.goecoder import fetch_city_values
from infrastructure.overpass_query_builder import compose_queries
from infrastructure.overpass_api import fetch_api_result
from infrastructure.formatters import format_api_result, format_results


# hardcoded company tag for now
# to simplify logic and skip translating user search term into corresponding overpass (api) tag
def find_companies(cities, company_tags=["it"]):
    cities = resolve_cities(cities)

    if not cities:
        return []

    queries = compose_queries(cities, company_tags)

    results = execute_queries(queries)
    
    formatted_results = format_results(results)
    # list of dictionary items with keys: name, website, domain

    return formatted_results


def resolve_cities(cities):
    cache = load_cache()

    updated = False
    requested_keys = [c.strip().lower() for c in cities]

    for key in requested_keys:
        if key not in cache:
            value = fetch_city_values(key)
            if value:
                cache[key] = value
                updated = True

    if updated:
        save_cache(cache)

    return {k: cache[k] for k in requested_keys if k in cache}


def execute_queries(queries):
    results = []

    for query in queries:
        raw = fetch_api_result(query)
        if raw:
            formatted = format_api_result(raw)
            results.extend(formatted)

    return results