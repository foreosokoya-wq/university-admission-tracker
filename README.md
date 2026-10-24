# University Admission Update Tracker

A Python project that monitors university websites for announcements, identifies potentially admission-related updates, and displays them in a Flask dashboard.

## Features

- Scrapes university announcement pages.
- Classifies announcements into categories such as application, admission list, direct entry, deadlines, and fees.
- Stores announcements in an SQLite database.
- Displays announcements in a Flask dashboard.
- Supports searching and filtering by university and category.
- Identifies announcements that may need manual review.

## Universities

The project currently targets these Nigerian universities:

- **AFIT** — Air Force Institute of Technology
- **UNILAG** — University of Lagos
- **UI** — University of Ibadan
- **OAU** — Obafemi Awolowo University
- **LAUTECH** — Ladoke Akintola University of Technology

The scrapers use official university announcement or news pages. Some sources contain general university news, not just admission notices.

## Technologies

- Python
- Flask
- Requests
- BeautifulSoup
- SQLite
- HTML, CSS and Jinja templates

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/foreosokoya-wq/university-admission-tracker
cd university_tracker
```

Replace `https://github.com/foreosokoya-wq/university-admission-tracker` with your repository's URL.

### 2. Create and activate a virtual environment

On Windows:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Update the announcements

```bash
python update_tracker.py
```

### 5. Start the dashboard

```bash
python app.py
```

Open the local address displayed in your terminal, usually `http://127.0.0.1:5000`.

## Current Limitations

- Website availability and page structure can change.
- Some announcements may not have publication dates.
- Classification is automated and may require manual review.
- Not every university's scraper has been fully integrated and tested through the complete tracker pipeline.

## Future Improvements

- Add more university sources.
- Improve admission-specific filtering and classification.
- Improve date extraction and duplicate detection.
- Add scheduled updates and notifications.

---

**Built as a hands-on Python project to learn web scraping, databases, text classification, and Flask application development.**