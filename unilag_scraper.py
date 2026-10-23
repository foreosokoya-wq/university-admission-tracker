from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin


def get_unilag_publication_date(article_url):
    response = requests.get(
        article_url,
        headers={
            "User-Agent": "UniversityUpdateTracker/1.0"
        },
        timeout=20,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    published = soup.select_one(
        'meta[property="article:published_time"]'
    )

    if published and published.get("content"):
        return published["content"]

    time_element = soup.select_one("time")

    if time_element:
        return time_element.get("datetime") or time_element.get_text(
            " ", strip=True
        )

    return None


def scrape_unilag_announcements():
    source_url = "https://unilag.edu.ng/category/important-notice/" 

    response = requests.get(
        source_url, headers={"User-Agent":"UniversityUpdateTracker/1.0"}, timeout=20

    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    print("Status Code: ", response.status_code)
    print("Title:", soup.title.get_text(strip=True) if soup.title else "Not found")
    
    announcements = []
    seen_url = set()

    for article in soup.select("article"):
        link = article.select_one(
            "h3 a, h2 a, .entry-title a, .post-title a "
        )
        if link is None:
            continue

        title = link.get_text(" ", strip=True)
        url = urljoin(source_url, link.get("href", ""))

        if not title or not url:
            continue

        seen_url.add(url)

        published_at = get_unilag_publication_date(url)
        
        announcements.append({
            "title": title,
            "url": url,
            "published_at": published_at
        })

    return announcements


if __name__ == "__main__":
    try:
        result = scrape_unilag_announcements()
        print(f"Retreived {len(result)} announcements.")

        for item in result:
            print("\nTitle: ", item['title'])
            print("URL: ", item['url'])
            print("Published: ", item['published_at'])

    except requests.RequestException as e:
        print(f"Could not retrieve UNILAG announcements: {e}")
    

    

