'import sqlite3
from datetime import date

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    goal TEXT,
    streak INTEGER DEFAULT 0,
    last_active TEXT
)
""")

conn.commit()


def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchone()


def add_user(user_id, goal):
    today = str(date.today())
    cursor.execute(
        "INSERT OR REPLACE INTO users (user_id, goal, streak, last_active) VALUES (?, ?, 0, ?)",
        (user_id, goal, today)
    )
    conn.commit()


def update_streak(user_id, success=True):
    user = get_user(user_id)
    if not user:
        return

    today = str(date.today())
    streak = user[2]
    last = user[3]

    if success:
        if last != today:
            streak += 1
    else:
        streak = 0

    cursor.execute(
        "UPDATE users SET streak=?, last_active=? WHERE user_id=?",
        (streak, today, user_id)
    )
    conn.commit()


def get_stats():
    cursor.execute("SELECT COUNT(*) FROM users")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(streak) FROM users")
    avg = cursor.fetchone()[0] or 0

    return total, round(avg, 1)'