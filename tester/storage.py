import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "runs.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            data TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_run(run):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO runs (timestamp, data) VALUES (?, ?)",
        (run["timestamp"], json.dumps(run)),
    )
    conn.commit()
    conn.close()


def list_runs(limit=20):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute(
        "SELECT data FROM runs ORDER BY id DESC LIMIT ?", (limit,)
    )
    rows = cur.fetchall()
    conn.close()
    return [json.loads(r[0]) for r in rows]
