import sqlite3

DB_PATH = "mental_wellness.db"

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

# USERS
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT,
    day_count INTEGER,
    chat_ready INTEGER
)
""")

# CHATS
cursor.execute("""
CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT,
    message TEXT
)
""")

# MOOD
cursor.execute("""
CREATE TABLE IF NOT EXISTS mood (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mood TEXT,
    date TEXT
)
""")

# APP STATE
cursor.execute("""
CREATE TABLE IF NOT EXISTS app_state (
    id INTEGER PRIMARY KEY,
    day_count INTEGER,
    chat_ready INTEGER
)
""")

cursor.execute("INSERT OR IGNORE INTO app_state VALUES (1, 1, 0)")

conn.commit()