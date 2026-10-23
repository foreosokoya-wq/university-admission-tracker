import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

URL = "https://afit.edu.ng/home/category/admission/" #"https://afit.edu.ng/home/"

HEADERS = {"User-Agent": "AdmissionTracker/1.0"}

def scrape_announcements(url=URL):
    try:
        response = requests.get(
            url, headers=HEADERS, timeout=15
        )
        response.raise_for_status()

    except requests.exceptions.ConnectionError:
        print("Could not connect to the server. Please check your internet or DNS")
        raise

    except requests.exceptions.Timeout:
        print("Took too long to respond")
        raise

    except requests.exceptions.HTTPError as e:
        print(f"An error occured: {e}")
        raise

    soup = BeautifulSoup(response.text, "html.parser")
    seen_url = set()
    announcements = []


    print(f"Status Code: {response.status_code}")
    print("Page Title:", soup.title.get_text(strip = True) if soup.title else "No Title Found")

    for post in soup.select("article.listing-item"):
        heading = post.select_one("h2.title")
        link = heading.find("a", href=True) if heading else None

        if not heading or not link:
            continue

        title = heading.get_text(" ", strip=True)
        article_url = urljoin(url, link['href'])

        url_parsed = urlparse(article_url)
        if url_parsed.scheme not in ['http', 'https']:
            continue

        if article_url in seen_url:
            continue
        
        date_element = post.select_one("time[datetime]")
        published_at = (
            date_element['datetime']
            if date_element
            else None
        )

        announcement = {
            "title": title,
            "url": article_url,
            "published_at": published_at
        }

        announcements.append(announcement)

        seen_url.add(article_url)

    return announcements




if __name__=="__main__":
    results = scrape_announcements(URL)

    print(len(results))

    for item in results:
        print(item)