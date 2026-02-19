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