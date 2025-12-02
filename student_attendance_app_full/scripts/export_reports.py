import csv
from pathlib import Path
from services.report_service import attendance_summary_by_course
from services.course_service import get_all_courses


def export_course_report(course_id: int, filename: str | None = None) -> str:
    if filename is None:
        filename = f"course_{course_id}_attendance_report.csv"

    output_path = Path(filename).resolve()
    data = attendance_summary_by_course(course_id)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["Student Name", "Present", "Absent", "Total", "Attendance Percentage"]
        )
        for d in data:
            writer.writerow(
                [
                    d["student_name"],
                    d["present_count"],
                    d["absent_count"],
                    d["total"],
                    d["percentage"],
                ]
            )

    return str(output_path)


if __name__ == "__main__":
    # Simple example: export for first course
    courses = get_all_courses()
    if not courses:
        print("No courses found. Please add a course first.")
    else:
        first_course_id = courses[0]["id"]
        path = export_course_report(first_course_id)
        print(f"Exported report to {path}")
