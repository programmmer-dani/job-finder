from urllib.parse import urlparse


def url_to_domain(url):
    if not url or not url.strip():
        return ""
    s = url.strip()
    if "://" not in s:
        s = "https://" + s
    return (urlparse(s).netloc or "").lower()
