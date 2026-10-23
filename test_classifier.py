import database as db
from scraper import scrape_announcements
from classifier import classify_announcement

db.initialise_db()
db.upgrade_db()

announcements = db.get_announcements()

for item in announcements:
    result = classify_announcement(item)
    db.save_classification(item['url'], result)

    print(f"\nTitle: {result['title']}")
    print(f"URL: {item['url']}")
    print(f"Category: {result['category']}")
    print(f"Relevance: {result['relevance']}")
    print(f"Reason: {result['reason']}")

print(f"\nClassified and saved {len(announcements)} announcements.")