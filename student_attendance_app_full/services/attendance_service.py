from typing import List, Dict, Any
from database.db_manager import get_connection
from utils.helpers import today_str
from utils.validators import validate_date_str


def enroll_student(student_id: int, course_id: int) -> tuple[bool, str]:
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)",
            (student_id, course_id),
        )
        conn.commit()
    except Exception as e:
        conn.close()
        return False, f"Error enrolling student: {e}"
    conn.close()
    return True, "Student enrolled successfully."


def get_enrolled_students(course_id: int) -> List[Dict[str, Any]]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT s.id, s.name, s.email
        FROM students s
        JOIN enrollments e ON e.student_id = s.id
        WHERE e.course_id = ?
        ORDER BY s.name
        """,
        (course_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "email": r[2]} for r in rows]


def mark_attendance(
    student_id: int, course_id: int, status: str, date_str: str | None = None
) -> tuple[bool, str]:
    if status not in ("Present", "Absent"):
        return False, "Status must be 'Present' or 'Absent'."

    if date_str is None or not date_str.strip():
        date_str = today_str()
    error = validate_date_str(date_str)
    if error:
        return False, error

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO attendance (student_id, course_id, date, status)
        VALUES (?, ?, ?, ?)
        """,
        (student_id, course_id, date_str, status),
    )
    conn.commit()
    conn.close()
    return True, "Attendance marked."


def get_attendance_for_course(
    course_id: int,
) -> List[Dict[str, Any]]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT a.id, s.name, a.date, a.status
        FROM attendance a
        JOIN students s ON s.id = a.student_id
        WHERE a.course_id = ?
        ORDER BY a.date, s.name
        """,
        (course_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return [
        {"id": r[0], "student_name": r[1], "date": r[2], "status": r[3]} for r in rows
    ]
