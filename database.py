import sqlite3

DB_NAME = "work_tracker.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        start_time TEXT,
        end_time TEXT,
        duration_seconds INTEGER DEFAULT 0,
        break_seconds INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)

    default_settings = {
        "break_alarm_enabled": "0",
        "break_alarm_minutes": "90",
        "break_alarm_type": "windows"
    }

    for key, value in default_settings.items():

        cursor.execute("""
        INSERT OR IGNORE INTO settings
        (key, value)
        VALUES (?, ?)
        """, (key, value))

    conn.commit()
    conn.close()


def get_setting(key, default_value=""):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT value
    FROM settings
    WHERE key = ?
    """, (key,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return default_value


def set_setting(key, value):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO settings
    (key, value)
    VALUES (?, ?)
    """, (key, str(value)))

    conn.commit()
    conn.close()