def get_user_input():
    cities = get_input("citie(s)")
    keywords = get_input("keyword(s)")
    return cities, keywords

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