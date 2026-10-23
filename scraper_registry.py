from scraper import scrape_announcements as scrape_afit
from unilag_scraper import scrape_unilag_announcements
from ui_scraper import scrape_ui_announcements

SCRAPERS = {
    "AFIT": scrape_afit,
    "UNILAG": scrape_unilag_announcements,
    "UI": scrape_ui_announcements
}

for university, scrape_func in SCRAPERS.items():
    print(university, "->", scrape_func.__name__)