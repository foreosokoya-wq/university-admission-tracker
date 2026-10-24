import re
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

SOURCE_URL = "https://oauife.edu.ng/news-and-events/"
def scrape_oau_announcements():
    response = requests.get(
        SOURCE_URL, headers={"User-Agent": "UniversityUpdateTracker/1.0"}, timeout=20
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    
    announcements = []
    seen_url = set()

    for heading in soup.select("h3 a, h2 a"):
        title = heading.get_text(" ", strip=True)
        url = urljoin(SOURCE_URL, heading.get("href", ""))

        if not title or "oauife.edu.ng" not in url:
            continue

        if url.rstrip("/") == SOURCE_URL.rstrip("/"):
            continue

        container = heading.parent.parent
        text = container.get_text(" ", strip=True)
        match = re.search(
            r"\b[A-Z][a-z]+ \d{1,2},? \d{4}\b", text
        )

        announcements.append({
            "title": title,
            "url": url,
            "published_at": match.group(0) if match else None
        })
        seen_url.add("url")

    unique = {item['url']: item for item in announcements}
    

    return list(unique.values())


if __name__ == "__main__":
    results = scrape_oau_announcements()
    print(f"Retrieved {len(results)} announcements")
    for item in results:
        print(item['title'], " | ", item['url'], " | ", item['published_at'])
    

        

        

