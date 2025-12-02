from typing import List, Dict, Any
from database.db_manager import get_connection


def attendance_summary_by_course(course_id: int) -> List[Dict[str, Any]]:
    """
    Returns list: [{student_name, present_count, absent_count, total, percentage}, ...]
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT s.name,
               SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) AS present_count,
               SUM(CASE WHEN a.status = 'Absent' THEN 1 ELSE 0 END) AS absent_count,
               COUNT(*) AS total
        FROM attendance a
        JOIN students s ON s.id = a.student_id
        WHERE a.course_id = ?
        GROUP BY s.id, s.name
        ORDER BY s.name
        """,
        (course_id,),
    )
    rows = cur.fetchall()
    conn.close()

    result: List[Dict[str, Any]] = []
    for name, present, absent, total in rows:
        percentage = (present / total * 100.0) if total else 0.0
        result.append(
            {
                "student_name": name,
                "present_count": present,
                "absent_count": absent,
                "total": total,
                "percentage": round(percentage, 2),
            }
        )
    return result
