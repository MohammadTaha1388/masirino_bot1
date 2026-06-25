import sqlite3

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS vip (
    user_id INTEGER PRIMARY KEY,
    is_vip INTEGER DEFAULT 0
)
""")

conn.commit()


def set_vip(user_id, status=True):
    cursor.execute(
        "INSERT OR REPLACE INTO vip (user_id, is_vip) VALUES (?, ?)",
        (user_id, int(status))
    )
    conn.commit()


def is_vip(user_id):
    cursor.execute("SELECT is_vip FROM vip WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    return result and result[0] == 1