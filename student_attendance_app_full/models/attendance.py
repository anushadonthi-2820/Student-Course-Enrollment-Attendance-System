from dataclasses import dataclass


@dataclass
class Attendance:
    id: int | None
    student_id: int
    course_id: int
    date: str
    status: str  # 'Present' or 'Absent'
