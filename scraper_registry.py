from scraper import scrape_announcements as scrape_afit
from unilag_scraper import scrape_unilag_announcements
from ui_scraper import scrape_ui_announcements
from oau_scraper import scrape_oau_announcements
from lautech_scraper import scrape_lautech_announcements

SCRAPERS = {
    "AFIT": scrape_afit,
    "UNILAG": scrape_unilag_announcements,
    "UI": scrape_ui_announcements,
    "OAU": scrape_oau_announcements,
    "LAUTECH": scrape_lautech_announcements
}

for university, scrape_func in SCRAPERS.items():
    print(university, "->", scrape_func.__name__)