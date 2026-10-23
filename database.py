import sqlite3

DB_NAME = "tracker.db"

def initialise_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS announcements(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            university TEXT NOT NULL DEFAULT 'AFIT',
            title TEXT NOT NULL,
            url TEXT NOT NULL UNIQUE,
            published_at TEXT,
            first_seen_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

def save_announcements(announcements, university="AFIT"):
    results = {
        "new": [],
        "changed": [],
        "unchanged": []
    }
    with sqlite3.connect(DB_NAME) as conn:
        for item in announcements:
            title = item['title']
            url = item['url']
            published_at = item.get('published_at')

            existing = conn.execute("""
                SELECT title, published_at FROM announcements
                WHERE url = ?
            """, (url,)).fetchone()

            if existing is None:
                conn.execute("""
                    INSERT INTO announcements
                    (university, title, url, published_at, last_checked_at)
                    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (university, title, url, published_at))

                results['new'].append(item)

            else:
                old_title, old_date = existing
                if (old_title != title or old_date != published_at):
                    conn.execute("""
                        UPDATE announcements
                        SET title = ?, published_at = ?, last_checked_at = CURRENT_TIMESTAMP, last_changed_at = CURRENT_TIMESTAMP
                        WHERE url = ?
                    """, (title, published_at, url))

                    results['changed'].append(item)

                else:
                    conn.execute("""
                        UPDATE announcements
                        SET last_checked_at = CURRENT_TIMESTAMP
                        WHERE url = ?
                    """, (url,))
                    results['unchanged'].append(item)
    return results


def get_announcements():
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row

        rows = conn.execute("""
            SELECT id, university, title, url, published_at, first_seen_at, category, relevance, reason FROM announcements
            ORDER BY first_seen_at DESC
        """).fetchall()
        return [dict(row) for row in rows]

def upgrade_db():
    with sqlite3.connect(DB_NAME) as conn:
        column = {
            row[1]
            for row in conn.execute(
                "PRAGMA table_info(announcements)"
            ).fetchall()
        }

        if "last_checked_at" not in column:
            conn.execute("""
                ALTER TABLE announcements
                ADD COLUMN last_checked_at TEXT
            """)

        if "last_changed_at" not in column:
            conn.execute("""
                ALTER TABLE announcements
                ADD COLUMN last_changed_at TEXT
            """)

        if "category" not in column:
            conn.execute("""
                ALTER TABLE announcements
                ADD COLUMN category TEXT
            """)

        if "relevance" not in column:
            conn.execute("""
                ALTER TABLE announcements
                ADD COLUMN relevance TEXT
            """)

        if "reason" not in column:
            conn.execute("""
                ALTER TABLE announcements
                ADD COLUMN reason TEXT
            """)


def save_classification(url, result):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            UPDATE announcements
            SET category = ?, relevance = ?, reason = ?
            WHERE url = ?
        """, (result['category'], result['relevance'], result['reason'], url))









