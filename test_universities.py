
from universities import UNIVERSITIES

for code, details in UNIVERSITIES.items():
    print(code, "-", details["name"])
    print("Scraper ready:", details["scraper_ready"])
    print()
