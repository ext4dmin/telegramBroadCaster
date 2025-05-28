import sqlite3
from config import DB_PATH

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

# Создание таблицы сообщений
cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    image_path TEXT,
    sent INTEGER NOT NULL DEFAULT 0
)
""")
conn.commit()


def add_message(text: str, image_path: str = None) -> int:
    cursor.execute(
        "INSERT INTO messages (text, image_path) VALUES (?, ?)",
        (text, image_path)
    )
    conn.commit()
    return cursor.lastrowid


def get_unsent_messages():
    cursor.execute(
        "SELECT id, text, image_path FROM messages WHERE sent = 0"
    )
    return cursor.fetchall()


def mark_sent(message_id: int):
    cursor.execute(
        "UPDATE messages SET sent = 1 WHERE id = ?",
        (message_id,)
    )
    conn.commit()