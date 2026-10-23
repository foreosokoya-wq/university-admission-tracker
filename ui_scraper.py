from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

SOURCE_URL = "https://ui.edu.ng/news"


def get_ui_publication_date(article_url):
    response = requests.get(
        article_url,
        headers={
            "User-Agent": "UniversityUpdateTracker/1.0"
        },
        timeout=20,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # First choice: publication date in metadata
    meta_date = soup.find(
        "meta",
        property="article:published_time"
    )

    if meta_date and meta_date.get("content"):
        return meta_date["content"]

    # Second choice: machine-readable date
    time_tag = soup.find("time")

    if time_tag:
        return time_tag.get("datetime") or time_tag.get_text(
            " ", strip=True
        )

    return None


def scrape_ui_announcements():
    response = requests.get(
        SOURCE_URL, headers={"User-Agent": "UniversityUpdateTracker/1.0"}, timeout=20
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    announcements = []
    seen_url = set()

    for row in soup.select("div.views-row"):
        heading = row.select_one("h4 a")

        if heading is None:
            continue

        title = heading.get_text(" ", strip=True)
        url = urljoin(SOURCE_URL, heading['href'])

        if not title or "/news/" not in url:
            continue

        published_at = get_ui_publication_date(url)
        
        announcements.append({
            "title": title,
            "url": url,
            "published_at": published_at
        })

        seen_url.add(url)

    return announcements

if __name__ == "__main__":
    results = scrape_ui_announcements()

    print(f"Retrieved: {len(results)} announcements")

    for item in results:
        print("\nTitle:", item["title"])
        print("URL:", item["url"])
        print("Published:", item["published_at"])



