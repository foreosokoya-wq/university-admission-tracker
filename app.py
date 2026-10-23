from flask import Flask, render_template, request, redirect, url_for, flash
from database import initialise_db, get_announcements, upgrade_db
from update_tracker import update_tracker
from universities import UNIVERSITIES

app = Flask(__name__)
app.secret_key = "secret-key"

initialise_db()
upgrade_db()

@app.route('/')
def index():
    announcements = get_announcements()

    selected_university = request.args.get("university", "")
    selected_category = request.args.get("category", "")
    search_query = request.args.get("q", "").strip()

    categories = sorted({
        item['category']
        for item in announcements
        if item['category']
    })

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

    return render_template('index.html', announcements=announcements, 
                           categories=categories, selected_category=selected_category, 
                           search_query=search_query, universities = UNIVERSITIES, 
                           selected_university = selected_university)
            
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