from flask import Flask, render_template, request, redirect, url_for, flash
from database import initialise_db, get_announcements, upgrade_db
from update_tracker import update_tracker
from universities import UNIVERSITIES
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY")

if not app.config["SECRET_KEY"]:
    raise RuntimeError(
        "FLASK_SECRET_KEY is not set. "
        "Set it in your environment before starting the app."
    )

initialise_db()
upgrade_db()

@app.route('/')
def index():
    all_announcements = get_announcements()
    announcements = all_announcements.copy()

    selected_university = request.args.get("university", "")
    selected_category = request.args.get("category", "")
    search_query = request.args.get("q", "").strip()

    categories = sorted({
        item['category']
        for item in all_announcements
        if item['category']
    })

    # Dashboard statistics use all announcements, even while filters are active.
    admission_categories = {"admission_list", "application", "direct_entry"}
    total_announcements = len(all_announcements)
    admission_related_count = sum(
        1 for item in all_announcements
        if item['category'] in admission_categories
    )
    deadline_count = sum(
        1 for item in all_announcements
        if item['category'] == "deadline"
    )
    ready_scrapers = sum(
        1 for details in UNIVERSITIES.values()
        if details.get("scraper_ready", False)
    )

    if selected_university:
        announcements = [
            item
            for item in announcements
            if item['university'] == selected_university
        ]

    if search_query:
        announcements = [
            item
            for item in announcements
            if search_query.lower() in item['title'].lower()
        ]

    if selected_category:
        announcements = [
            item
            for item in announcements
            if item['category'] == selected_category
        ]

    return render_template(
        'index.html',
        announcements=announcements,
        total_announcements=total_announcements,
        admission_related_count=admission_related_count,
        deadline_count=deadline_count,
        ready_scrapers=ready_scrapers,
        categories=categories,
        selected_category=selected_category,
        search_query=search_query,
        universities=UNIVERSITIES,
        selected_university=selected_university
    )
            
@app.route("/refresh", methods=["POST"])
def refresh():
    try:
        result = update_tracker()
        if result is None:
            flash("No announcements were retrieved!")

        else:
            flash(
                f"Update Complete! New {result['new']}, "
                f"Changed: {result['changed']}, "
                f"Unchanged: {result['unchanged']}"
            )

    except Exception:
        app.logger.exception("Tracker update failed!")
        flash("The update failed! Check the terminal for details")

    return redirect(url_for("index"))




if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)