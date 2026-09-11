import sqlite3

DB_NAME = "applications.db"


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            status TEXT NOT NULL,
            application_date TEXT NOT NULL,
            notes TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_application(company, role, status, application_date, notes):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO applications
        (company, role, status, application_date, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (
        company,
        role,
        status,
        application_date,
        notes
    ))

    conn.commit()
    conn.close()


def get_applications():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, company, role, status, application_date, notes
        FROM applications
        ORDER BY id DESC
    """)

    applications = cursor.fetchall()

    conn.close()

    return applications


def delete_application(application_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM applications WHERE id = ?",
        (application_id,)
    )

    conn.commit()
    conn.close()