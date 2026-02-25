def get_cities():
    raw = input("Cities (comma-separated): ").strip()
    while True:
        cities = [c.strip() for c in raw.split(",") if c.strip()]
        if not cities:
            raw = input("Enter at least one city: ").strip()
            continue
        print("  You entered:", ", ".join(cities))
        confirm = input("Confirm? (y) or type to edit: ").strip().lower()
        if confirm in ("y", "yes"):
            return cities
        if confirm:
            raw = confirm
            
def show_results(companies):
    for company in companies:
        print("\n\n--------companies sorted from most potential match to least-----------\n\n")
        # TODO: Add city to the output and to the companies dictionary: {company["city"]} - 
        if company["career_page"] != "":
            print(f"{company["name"]} - {company["career_page"]}")
        else:
            print(f"{company["name"]} - {company["website"]}")