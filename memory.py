from datetime import date
import hashlib
from database import conn, cursor


# ---------------- PASSWORD ----------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ---------------- USER ----------------
def create_user(username, password):
    hashed = hash_password(password)

    cursor.execute(
        "INSERT INTO users (username, password, day_count, chat_ready) VALUES (?, ?, ?, ?)",
        (username, hashed, 1, 0)
    )
    conn.commit()


def get_user(username, password):
    hashed = hash_password(password)

    cursor.execute(
        "SELECT day_count, chat_ready FROM users WHERE username=? AND password=?",
        (username, hashed)
    )

    row = cursor.fetchone()

    if row:
        return {
            "day_count": row[0],
            "chat_ready": bool(row[1])
        }
    return None


def user_exists(username):
    cursor.execute(
        "SELECT username FROM users WHERE username=?",
        (username,)
    )
    return cursor.fetchone() is not None


def update_user(username, day_count, chat_ready):
    cursor.execute(
        "UPDATE users SET day_count=?, chat_ready=? WHERE username=?",
        (day_count, int(chat_ready), username)
    )
    conn.commit()


# ---------------- APP STATE ----------------
def save_app_state(day_count, chat_ready):
    cursor.execute(
        "UPDATE app_state SET day_count=?, chat_ready=? WHERE id=1",
        (day_count, int(chat_ready))
    )
    conn.commit()


def load_app_state():
    cursor.execute(
        "SELECT day_count, chat_ready FROM app_state WHERE id=1"
    )

    row = cursor.fetchone()

    if row:
        return {
            "day_count": row[0],
            "chat_ready": bool(row[1])
        }

    return None


# ---------------- CHAT ----------------
def save_chat(role, message):
    cursor.execute(
        "INSERT INTO chats (role, message) VALUES (?, ?)",
        (role, message)
    )
    conn.commit()


# ---------------- MOOD ----------------
def save_mood(mood):
    today = str(date.today())

    cursor.execute(
        "INSERT INTO mood (mood, date) VALUES (?, ?)",
        (mood, today)
    )
    conn.commit()


def get_today_mood():
    today = str(date.today())

    cursor.execute(
        "SELECT mood FROM mood WHERE date=? ORDER BY id DESC LIMIT 1",
        (today,)
    )

    row = cursor.fetchone()
    return row[0] if row else None


def get_all_moods():
    cursor.execute("SELECT mood FROM mood ORDER BY id DESC")
    rows = cursor.fetchall()

    return [r[0] for r in rows] if rows else []


# ---------------- CBT ----------------
def save_thought(negative, positive):
    cursor.execute(
        "INSERT INTO chats (role, message) VALUES (?, ?)",
        ("cbt", f"{negative} -> {positive}")
    )
    conn.commit()


# ---------------- FIRST TIME USER ----------------
def is_first_time_user():
    cursor.execute("SELECT COUNT(*) FROM chats")
    count = cursor.fetchone()[0]

    return count < 5