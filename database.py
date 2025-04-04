import sqlite3
from datetime import datetime
from typing import List, Dict

DATABASE_NAME = "calls.db"

def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            call_sid TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            user_input TEXT,
            ai_response TEXT,
            status TEXT DEFAULT 'initiated',
            outcome TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_call(call_sid: str, user_input: str, ai_response: str):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO calls (call_sid, user_input, ai_response)
        VALUES (?, ?, ?)
    """, (call_sid, user_input, ai_response))
    conn.commit()
    conn.close()

def update_call_status(call_sid: str, status: str, outcome: str = None):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE calls
        SET status = ?, outcome = ?
        WHERE call_sid = ?
    """, (status, outcome, call_sid))
    conn.commit()
    conn.close()

def get_call_logs(limit: int = 100) -> List[Dict]:
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM calls
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results

# Initialize database on import
init_db()