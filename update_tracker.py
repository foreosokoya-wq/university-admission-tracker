
from scraper_registry import SCRAPERS
from classifier import classify_announcement
from database import (
    initialise_db,
    upgrade_db,
    save_announcements,
    get_announcements,
    save_classification,
)


def update_tracker():
    initialise_db()
    upgrade_db()

    totals = {
        "retrieved": 0,
        "new": 0,
        "changed": 0,
        "unchanged": 0,
        "classified": 0,
    }

    failures = {}

    # Step 1: Scrape each registered university.
    for university, scrape_function in SCRAPERS.items():
        print(f"\nChecking {university}...")

        try:
            announcements = scrape_function()
        except Exception as error:
            failures[university] = str(error)
            print(f"{university} scraper failed: {error}")
            continue

        print(f"{university}: retrieved {len(announcements)}")

        if not announcements:
            print(f"No announcements retrieved from {university}.")
            continue

        # Step 2: Save them under the correct university.
        results = save_announcements(
            announcements,
            university=university,
        )

        totals["retrieved"] += len(announcements)

        for result_type in ("new", "changed", "unchanged"):
            totals[result_type] += len(results[result_type])

    # Step 3: Classify stored announcements.
    stored_announcements = get_announcements()

    for item in stored_announcements:
        try:
            result = classify_announcement(item)
            save_classification(item["url"], result)
            totals["classified"] += 1
        except Exception as error:
            print(
                f"Classification failed for "
                f"{item['title']}: {error}"
            )

    # Step 4: Report the overall results.
    print("\n--- UPDATE SUMMARY ---")

    for key, value in totals.items():
        print(f"{key.title()}: {value}")

    if failures:
        print("\nUniversities that failed:")
        for university, error in failures.items():
            print(f"- {university}: {error}")

    if totals["retrieved"] == 0:
        return None

    return totals


if __name__ == "__main__":
    update_tracker()
