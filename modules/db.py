import sqlite3


def create_database():
    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS reports (
                        id INTEGER PRIMARY KEY,
                        report_uuid TEXT,
                        scan_status TEXT
                    )''')
    conn.commit()
    conn.close()


def started(report_uuid):
    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reports (report_uuid, scan_status) VALUES (?, ?)", (report_uuid, "started"))
    conn.commit()
    conn.close()


def error(report_uuid, error_text):
    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()
    error_text = "error : " + error_text
    cursor.execute("INSERT INTO reports (report_uuid, scan_status) VALUES (?, ?)", (report_uuid, error_text))
    conn.commit()
    conn.close()


def completed(report_uuid):
    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reports (report_uuid, scan_status) VALUES (?, ?)", (report_uuid, "completed"))
    conn.commit()
    conn.close()


def delete_report(report_uuid):
    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reports WHERE report_uuid = ?", (report_uuid,))
    conn.commit()
    conn.close()


def get_status(report_uuid):
    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()
    cursor.execute("SELECT scan_status FROM reports WHERE report_uuid = ?", (report_uuid,))
    scan_status = cursor.fetchone()
    conn.close()
    return scan_status[0] if scan_status is not None else None
