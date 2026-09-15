import sqlite3
import os
from datetime import datetime

# Absolute path relative to this file to prevent file path errors regardless of execution directory
DB_PATH = os.path.join(os.path.dirname(__file__), "waste_detection.db")


def get_connection():
    """Create a database connection and enable column access by name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_database():
    """Create the database and detections table if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_name TEXT NOT NULL,
            waste_type TEXT NOT NULL,
            confidence REAL NOT NULL,
            detected_at TEXT NOT NULL,
            bbox_coords TEXT DEFAULT ''
        )
    """)

    conn.commit()
    conn.close()


def add_detection(image_name, waste_type, confidence, bbox_coords=""):
    """Save a detection record to the database."""
    conn = get_connection()
    cursor = conn.cursor()

    detected_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO detections (image_name, waste_type, confidence, detected_at, bbox_coords)
        VALUES (?, ?, ?, ?, ?)
    """, (image_name, waste_type, float(confidence), detected_at, str(bbox_coords)))

    conn.commit()
    record_id = cursor.lastrowid
    conn.close()
    return record_id


def get_all_detections():
    """Retrieve all detection records from the database as list of dictionaries."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM detections
        ORDER BY detected_at DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    # Converts rows to standard python dictionaries for easy display in Streamlit and Pandas
    return [dict(row) for row in rows]


def delete_detection(detection_id):
    """Delete a detection record from the database."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM detections
        WHERE id = ?
    """, (detection_id,))

    conn.commit()
    conn.close()