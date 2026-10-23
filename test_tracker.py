from scraper import scrape_announcements
import database as db

db.initialise_db()
db.upgrade_db()

announcements = scrape_announcements()

results = db.save_announcements(announcements)
#print(f"Scraped {len(announcements)} announcements")

saved = db.get_announcements()
#print(f"Total announcements saved: {len(saved)}")

#for item in saved:
#    print(item["title"], "--", item['url'])

print(f"New: {len(results['new'])}")
print(f"Changed: {len(results['changed'])}")
print(f"Unchanged: {len(results['unchanged'])}")