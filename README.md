# Job Finder

A CLI tool that finds companies in chosen cities, discovers their career pages, and checks whether they list positions matching your keywords. Results are ordered by relevance (keyword match → has career page → other). Built as a portfolio project to demonstrate layered architecture, external APIs, and web scraping.
The tool can run for several minutes before finishing execution.

---

## How to use

**Requirements:** Python 3, and dependencies from `requirements.txt`. Geocoding uses `geopy` (add to your environment if not already installed).

```bash
pip install -r requirements.txt
# If geocoding fails: pip install geopy

cd /path/to/job-finder
python src/main.py
```

**Flow:**

1. **Cities** – Enter one or more cities (comma-separated), e.g. `Amsterdam, Berlin`. Confirm or edit.
2. **Keywords** – Enter job keywords to search for on career pages (comma-separated), e.g. `python, backend, intern`. Confirm or edit.
3. **Sector** – Pick one or more sectors by number (e.g. `1` for IT, `1, 2` for IT and Law). Confirm or edit.

The app then:

- Resolves city coordinates (using cached data or Nominatim),
- Fetches companies from OpenStreetMap (Overpass API) for those cities and sectors,
- Finds career pages per company (URL fuzzing, then homepage link discovery if needed),
- Fetches each career page and checks if any of your keywords appear,
- Sorts companies: **potential match** (keyword found) → **has career page** → **others**,
- Prints the list with name and career page (or website) URL.

**Example output:**

```
--------companies sorted from most potential match to least-----------

Company A - https://company-a.com/careers
Company B - https://company-b.com
...
```

---

## What is done

| Area | What it does |
|------|----------------|
| **Company discovery** | Gets companies from OpenStreetMap by city and sector (office type). Uses geocoding for city bounding boxes and Overpass for nodes with `office` + `website`. Results are deduplicated by domain and normalised to `name`, `website`, `domain`. |
| **Career page discovery** | For each company website, finds a career page URL. Two strategies: (1) **Fuzzing** – try common paths (`/careers`, `/jobs`, `/en/careers`, etc.); (2) **Link discovery** – fetch homepage, parse links, pick same-domain links whose path or text matches career-related keywords (multiple languages). First successful URL per company is stored. |
| **Job matching** | For companies with a career page, fetches the page HTML and checks whether any of the user’s keywords appear (case-insensitive). No parsing of job listings; simple substring presence. |
| **Prioritisation** | Companies are ordered into three buckets: **potential match** (keyword found on career page), **has career page** (no keyword match), **other** (no career page). Result list is concatenated in that order. |
| **CLI** | Prompts for cities, keywords, and sector(s). Sectors are chosen from a fixed list of 11 OSM `office` types (IT, law, insurance, real estate, etc.) so users don’t need to know API tags. Results are printed as name + URL. |

---

## APIs used

- **Nominatim (OpenStreetMap)** – Geocoding: city name → latitude, longitude, bounding box. Used to get a bbox per city for Overpass. Rate-limited and cached in `data/city_cache.json` so we don’t re-query for the same city.
- **Overpass API** – Query: “nodes with `office` = chosen tag(s) and `website`, inside this bbox”. One query per (city bbox, office tag). Returns OSM elements; infrastructure formatters turn them into company dicts (`name`, `website`, `domain`).

Company tags are OSM `office` values (e.g. `it`, `lawyer`, `insurance`). The CLI shows human-readable sector names and maps the user’s choice to these tags so the user doesn’t need to know the API.

## Scraper (career page discovery)

Lives in **infrastructure** because it does HTTP and HTML parsing.

- **Fuzzing** – Builds a list of candidate URLs (e.g. `base + "/careers"`, `base + "/en/jobs"`). Requests each until one returns 200 with non-empty body; that URL is the career page. Stops at first hit. Handles timeouts and connection errors without failing the whole run.
- **Link discovery** – If fuzzing finds nothing: fetch homepage, parse with BeautifulSoup, collect `<a href>`, resolve to absolute same-domain URLs. Keep links whose path or text contains career-related keywords (EN, ES, FR, DE, IT, PT, NL, PL, Nordic). Return the first such URL (or none). Connection errors result in an empty list so the pipeline continues.

Both strategies return a single URL per company; the orchestrator only needs “a” career page to run the keyword check.

## Other logic

- **City cache** – JSON file keyed by normalised city name (lowercase). Values: `lat`, `lon`, `bbox`. Missing cities are fetched via Nominatim and written back so repeat runs are fast and respectful of rate limits.
- **Deduplication** – Companies from Overpass are deduplicated by domain (via `url_to_domain`) so the same company in multiple cities or tags appears once.

---

## Project layout

```
src/
  main.py                 # Entry point → orchestrator.run()
  application/
    orchestrator.py       # Run pipeline: input → discover → career pages → match → sort → output
  presentation/
    cli.py                # get_user_input (cities, keywords, sectors), show_results
  domain/
    company_discovery.py   # find_companies, resolve_cities, execute_queries
    job_matcher.py         # search_matching_position (keywords in content)
    company_prioritiser.py # sort_companies (potential match / career page / other)
  infrastructure/
    overpass_api.py        # POST query to Overpass
    overpass_query_builder.py  # Build bbox + office-tag queries
    goecoder.py            # Nominatim geocode → lat, lon, bbox
    cache_repository.py    # load/save city cache (JSON)
    formatters.py          # OSM elements → company dicts, dedupe by domain
    scraper.py             # find_career_pages, fuzzing, link_scraper
    html_extractor.py      # fetch_html (URL → HTML string)
  utils/
    domain_extractor.py    # url_to_domain (for dedupe and same-domain links)
data/
  city_cache.json          # City name → { lat, lon, bbox }
```
