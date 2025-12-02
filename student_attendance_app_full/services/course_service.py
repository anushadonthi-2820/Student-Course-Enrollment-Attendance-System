from typing import List, Dict, Any
from database.db_manager import get_connection
from utils.validators import validate_non_empty


def create_course(name: str, code: str) -> tuple[bool, str]:
    error = validate_non_empty(name, "Course name") or validate_non_empty(
        code, "Course code"
    )
    if error:
        return False, error

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO courses (name, code) VALUES (?, ?)",
            (name.strip(), code.strip().upper()),
        )
        conn.commit()
    except Exception as e:
        conn.close()
        return False, f"Error creating course: {e}"
    conn.close()
    return True, "Course created successfully."


def get_all_courses() -> List[Dict[str, Any]]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, code FROM courses ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "code": r[2]} for r in rows]


def delete_course(course_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM courses WHERE id = ?", (course_id,))
    conn.commit()
    conn.close()
