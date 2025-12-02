# Student Course Enrollment & Attendance System

A small Python project using **Tkinter GUI** and **SQLite** (SQL database) to manage:

- Students
- Courses
- Enrollments
- Daily attendance
- Attendance summary reports

## Tech Stack

- Python 3.x
- Tkinter (built-in GUI library)
- SQLite (via `sqlite3` – built-in)
- Simple modular architecture (database, models, services, utils, gui, scripts)

## Features

- Add / view / delete students
- Add / view / delete courses
- Enroll students into courses
- Mark attendance (Present / Absent) for a date
- View attendance summary per course (percentage)
- Export attendance report to CSV (`scripts/export_reports.py`)

## How to Run

1. Make sure you have **Python 3** installed.
2. Extract this folder.
3. Open terminal / CMD in the project root.
4. Run:

   ```bash
   python main.py
   ```

5. The Tkinter window will open.

## Notes

- Database file: `school.db` is created automatically in the project root.
- Default date format: `YYYY-MM-DD`.
