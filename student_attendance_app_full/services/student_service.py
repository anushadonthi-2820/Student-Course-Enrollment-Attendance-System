from typing import List, Dict, Any
from database.db_manager import get_connection
from utils.helpers import today_str
from utils.validators import validate_non_empty, validate_email


def create_student(name: str, email: str = "", phone: str = "") -> tuple[bool, str]:
    error = validate_non_empty(name, "Student name")
    if error:
        return False, error

    email_error = validate_email(email)
    if email_error:
        return False, email_error

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students (name, email, phone, created_at) VALUES (?, ?, ?, ?)",
        (name.strip(), email.strip(), phone.strip(), today_str()),
    )
    conn.commit()
    conn.close()
    return True, "Student created successfully."


def get_all_students() -> List[Dict[str, Any]]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, phone, created_at FROM students ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return [
        {
            "id": r[0],
            "name": r[1],
            "email": r[2],
            "phone": r[3],
            "created_at": r[4],
        }
        for r in rows
    ]


def delete_student(student_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()
