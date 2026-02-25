def sort_companies(companies):
    sorted_companies = []
    matching_companies = []
    career_page_companies = []
    other_companies = []

    for company in companies:
        if company["potential_match"]:
            matching_companies.append(company)
        elif company["career_page"] != "":
            career_page_companies.append(company)
        else:
            other_companies.append(company)

    sorted_companies = matching_companies + career_page_companies + other_companies
    print(sorted_companies)
    return sorted_companies
