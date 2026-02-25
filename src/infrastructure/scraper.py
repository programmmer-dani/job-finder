from bs4 import BeautifulSoup
import requests
import urllib.parse as urlparse


def find_career_pages(companies):
    for company in companies:
        career_page = career_page_fuzzing(company["website"])
        if career_page != "":
            company["career_page"] = career_page
        else:
            career_page = career_page_scraping(company["website"])
            if career_page != "":
                company["career_page"] = career_page
        #print(company["name"], company["career_page"])
    return companies


def career_page_scraping(website):  # needs to return found career page | ""
    keywords = [
        # English
        "careers",
        "career",
        "jobs",
        "job",
        "vacancies",
        "vacancy",
        "work",
        "work-with-us",
        "join-us",
        "join",
        "opportunities",
        "opportunity",
        "recruitment",
        "recruit",
        "employment",
        "employ",
        "positions",
        "position",
        "hiring",
        "hire",
        "openings",
        "open-positions",
        "openings",
        "talent",
        "apply",
        "applications",
        "life-at",
        "our-team",
        "join-our-team",
        "we-are-hiring",
        "grow-with-us",
        # Spanish
        "carreras",
        "trabajos",
        "empleo",
        "vacantes",
        "oportunidades",
        "reclutamiento",
        "unete",
        # French
        "carrieres",
        "carrière",
        "emplois",
        "emploi",
        "postes",
        "recrutement",
        "opportunites",
        "rejoignez",
        # German
        "karriere",
        "stellen",
        "stellenangebote",
        "jobs",
        "arbeiten",
        "einstieg",
        "mitarbeiter",
        # Italian
        "carriera",
        "lavori",
        "lavoro",
        "posizioni",
        "reclutamento",
        "opportunita",
        "unisciti",
        # Portuguese
        "carreiras",
        "vagas",
        "trabalhos",
        "emprego",
        "oportunidades",
        "recrutamento",
        "junte-se",
        # Dutch
        "carriere",
        "banen",
        "vacatures",
        "werken",
        "solliciteren",
        # Polish
        "kariera",
        "praca",
        "oferty",
        "rekrutacja",
        "zatrudnienie",
        # Nordic (Swedish, Danish, Norwegian)
        "karriar",
        "jobb",
        "lediga",
        "stillinger",
        "stillingsannonser",
        "bli-med",
        # Other
        "vacature",
        "stellenmarkt",
        "arbeit",
        "offene-stellen",
        "jobs-bei",
    ]

    all_foundLinks = link_scraper(website)

    for link in all_foundLinks:
        for keyword in keywords:
            if keyword in link:
                return link
    return ""


def link_scraper(website):
    result = []
    try:
        response = requests.get(website, timeout=5)
    except requests.exceptions.RequestException:
        # TODO:log error (no links found)
        return result

    if response.status_code == 200 and response.text:
        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.find_all("a"):
            href = link.get("href")
            if href:
                result.append(urlparse.urljoin(website, href))
    return result


def career_page_fuzzing(website):
    # optional improvement:
    # recognise the country of of the cities(s), fuzz specifically for that country(ies)
    variations = [
        website + "/careers",
        website + "/career",
        website + "/careers-page",
        website + "/jobs",
        website + "/job",
        website + "/vacancies",
        website + "/work",
        website + "/work-with-us",
        website + "/join-us",
        website + "/opportunities",
        website + "/recruitment",
        website + "/employment",
        website + "/open-positions",
        website + "/positions",
        website + "/en/careers",
        website + "/en/jobs",
        website + "/es/careers",
        website + "/es/jobs",
        website + "/fr/careers",
        website + "/fr/jobs",
        website + "/de/careers",
        website + "/de/jobs",
        website + "/it/careers",
        website + "/it/jobs",
        website + "/pt/careers",
        website + "/pt/jobs",
        website + "/nl/careers",
        website + "/nl/jobs",
        website + "/pl/careers",
        website + "/pl/jobs",
        website + "/ru/careers",
        website + "/ru/jobs",
    ]
    for url in variations:
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200 and response.text:
                return url
        except requests.exceptions.RequestException:
            continue
    return ""
