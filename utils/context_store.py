import sqlite3
from threading import Lock
from typing import Optional

# Ensure thread-safety with a lock if your app is multi-threaded
lock = Lock()

# Initialize SQLite connection (file stored in project root)
conn = sqlite3.connect("user_context.db", check_same_thread=False)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_context (
    user_id TEXT PRIMARY KEY,
    context TEXT
)
""")
conn.commit()

def save_user_context(user_id: str, context: str):
    """Save or update user context string in the database."""
    with lock:
        cursor.execute(
            "REPLACE INTO user_context (user_id, context) VALUES (?, ?)",
            (user_id, context)
        )
        conn.commit()

def load_user_context(user_id: str) -> Optional[str]:
    """Load the context string for a user, or None if not found."""
    with lock:
        cursor.execute(
            "SELECT context FROM user_context WHERE user_id = ?",
            (user_id,)
        )
        row = cursor.fetchone()
        return row[0] if row else None
