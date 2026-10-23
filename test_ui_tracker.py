
import requests
from bs4 import BeautifulSoup

url = "https://ui.edu.ng/news/university-ibadan-ibadan-undergraduate-admissions-unit-20262027-admission-exercise-cut-marks"

response = requests.get(
    url,
    headers={"User-Agent": "UniversityUpdateTracker/1.0"},
    timeout=20,
)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

print("Page title:", soup.title.get_text(strip=True))

# Find the main page content
main = soup.find("main") or soup.find(id="main-content")

if main:

    # Find the main content using Drupal's page structure
    for selector in [
        ".region-content",
        ".block-system-main-block",
        ".node--type-news-events",
        ".field--name-body",
    ]:
        elements = soup.select(selector)

        print(f"\nSelector: {selector}")
        print(f"Matches: {len(elements)}")

        for element in elements[:2]:
            print(element.prettify()[:2500])

else:
    print("Could not find the main content container.")
