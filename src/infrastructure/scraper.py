import requests

# scrape company websites for career pages
def scrape_company_websites(companies):
    result = []
    for company in companies:
        copy = dict(company)
        career_page = scrape_career_page_fuzzing(copy["website"])
        
        print(career_page)
        
        copy["career_page"] = career_page
        result.append(copy)
    return result

def scrape_career_page_fuzzing(website):
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
            response = requests.get(url, timeout=5)
            if response.status_code == 200 and response.text:
                return url
        except requests.exceptions.RequestException:
            continue
    return ""
