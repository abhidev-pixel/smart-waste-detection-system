import sqlite3
from datetime import datetime

DATABASE_NAME = "database/waste_detection.db"


def create_database():
    """Create the database and detections table if they don't exist."""

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_name TEXT NOT NULL,
            waste_type TEXT NOT NULL,
            confidence REAL NOT NULL,
            detected_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
def add_detection(image_name, waste_type, confidence):
    """Save a detection record to the database."""

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    detected_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO detections (image_name, waste_type, confidence, detected_at)
        VALUES (?, ?, ?, ?)
    """, (image_name, waste_type, confidence, detected_at))

    conn.commit()
    conn.close()
def get_all_detections():
    """Retrieve all detection records from the database."""

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM detections
        ORDER BY detected_at DESC
    """)

    records = cursor.fetchall()

    conn.close()

    return records
def delete_detection(detection_id):
    """Delete a detection record from the database."""

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM detections
        WHERE id = ?
    """, (detection_id,))

    conn.commit()
    conn.close()
   