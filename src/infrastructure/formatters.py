from utils.domain_extractor import url_to_domain


def format_api_result(result):
    return (result or {}).get("elements", [])


def format_results(results):
    companies = []
    seen = set()
    for result in results:
        tags = result.get("tags") or {}
        website = (tags.get("website") or tags.get("contact:website") or "").strip()
        if not website:
            continue
        domain = url_to_domain(website)
        if not domain or domain in seen:
            continue
        seen.add(domain)
        companies.append(
            {
                "name": (tags.get("name") or "").strip() or "—",
                "website": website,
                "domain": domain,
            }
        )
    return companies
