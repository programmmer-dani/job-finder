def get_user_input():
    cities = get_input("citie(s)")
    keywords = get_input("keyword(s)")
    company_tags = get_company_tags()
    return cities, keywords, company_tags

SECTORS = [
    ("it", "IT / Software"),
    ("lawyer", "Law"),
    ("insurance", "Insurance"),
    ("estate_agent", "Real estate"),
    ("government", "Government"),
    ("association", "Association"),
    ("financial", "Financial"),
    ("accounting", "Accounting"),
    ("travel_agent", "Travel"),
    ("notary", "Notary"),
]

def get_company_tags():
    for i, (tag, label) in enumerate(SECTORS, 1):
        print(f"  {i}. {label}")
    raw = input("Sector number(s), comma-separated (e.g. 1, 2): ").strip()
    while True:
        try:
            indices = [int(s.strip()) for s in raw.split(",") if s.strip()]
            tags = [SECTORS[i - 1][0] for i in indices if 1 <= i <= len(SECTORS)]
        except (ValueError, IndexError):
            tags = []
        if not tags:
            print("  Enter at least one number from the list.")
            raw = input("Sector number(s), comma-separated (e.g. 1, 2): ").strip()
            continue
        print("  You selected:", ", ".join(tags))
        confirm = input("Confirm? (y) or type to edit: ").strip().lower()
        if confirm in ("y", "yes"):
            return tags
        if confirm:
            raw = confirm

def get_input(type):
    raw = input(f"Enter one or more {type} (comma-separated): ").strip()
    while True:
        user_input = [element.strip() for element in raw.split(",") if element.strip()]
        if not user_input:
            raw = input(f"Enter at least one {type}: ").strip()
            continue
        print("  You entered:", ", ".join(user_input))
        confirm = input("Confirm? (y) or type to edit: ").strip().lower()
        if confirm in ("y", "yes"):
            return user_input
        if confirm:
            raw = confirm
            
def show_results(companies):
    print("\n\n--------companies sorted from most potential match to least-----------\n\n")

    for company in companies:
        # TODO: Add city to the output and to the companies dictionary: {company["city"]} - 
        if company["career_page"] != "":
            print(f"{company["name"]} - {company["career_page"]}")
        else:
            print(f"{company["name"]} - {company["website"]}")