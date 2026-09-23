
import sqlite3
from datetime import datetime


DB_NAME = "oa_data.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            patient_id TEXT PRIMARY KEY,
            name TEXT,
            age INTEGER,
            gender TEXT,
            bmi REAL,
            occupation TEXT,
            location TEXT,
            risk_score INTEGER,
            risk_level TEXT,
            date_time TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_patient(data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO patients (
            patient_id,
            name,
            age,
            gender,
            bmi,
            occupation,
            location,
            risk_score,
            risk_level,
            date_time
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["patient_id"],
        data["name"],
        data["age"],
        data["gender"],
        data["bmi"],
        data["occupation"],
        data["location"],
        data["risk_score"],
        data["risk_level"],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_all_patients():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            patient_id,
            name,
            age,
            gender,
            bmi,
            occupation,
            location,
            risk_score,
            risk_level,
            date_time
        FROM patients
        ORDER BY date_time DESC
    """)

    patients = cursor.fetchall()

    conn.close()

    return patients


def get_patient(patient_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            patient_id,
            name,
            age,
            gender,
            bmi,
            occupation,
            location,
            risk_score,
            risk_level,
            date_time
        FROM patients
        WHERE patient_id = ?
    """, (patient_id,))

    patient = cursor.fetchone()

    conn.close()

    return patient


def delete_patient(patient_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM patients
        WHERE patient_id = ?
    """, (patient_id,))

    conn.commit()
    conn.close()


create_database()
