import tkinter as tk
from tkinter import ttk, messagebox

from services.student_service import create_student, get_all_students, delete_student
from services.course_service import create_course, get_all_courses, delete_course
from services.attendance_service import (
    enroll_student,
    get_enrolled_students,
    mark_attendance,
)
from services.report_service import attendance_summary_by_course
from utils.helpers import today_str


class StudentAttendanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Course Enrollment & Attendance System")
        self.geometry("900x600")

        self._create_widgets()

    # -------------------------- MAIN UI -------------------------- #
    def _create_widgets(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.student_frame = ttk.Frame(notebook)
        self.course_frame = ttk.Frame(notebook)
        self.attendance_frame = ttk.Frame(notebook)
        self.report_frame = ttk.Frame(notebook)

        notebook.add(self.student_frame, text="Students")
        notebook.add(self.course_frame, text="Courses")
        notebook.add(self.attendance_frame, text="Attendance")
        notebook.add(self.report_frame, text="Reports")

        self._build_student_tab()
        self._build_course_tab()
        self._build_attendance_tab()
        self._build_report_tab()

    # -------------------------- STUDENT TAB -------------------------- #
    def _build_student_tab(self):
        frm = self.student_frame

        form = ttk.LabelFrame(frm, text="Add Student")
        form.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(form, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(form, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(form, text="Phone:").grid(row=2, column=0, padx=5, pady=5, sticky="e")

        self.student_name_var = tk.StringVar()
        self.student_email_var = tk.StringVar()
        self.student_phone_var = tk.StringVar()

        ttk.Entry(form, textvariable=self.student_name_var, width=30).grid(
            row=0, column=1, padx=5, pady=5
        )
        ttk.Entry(form, textvariable=self.student_email_var, width=30).grid(
            row=1, column=1, padx=5, pady=5
        )
        ttk.Entry(form, textvariable=self.student_phone_var, width=30).grid(
            row=2, column=1, padx=5, pady=5
        )

        ttk.Button(form, text="Add Student", command=self._add_student).grid(
            row=3, column=0, columnspan=2, pady=10
        )

        list_frame = ttk.LabelFrame(frm, text="Students")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.student_tree = ttk.Treeview(
            list_frame,
            columns=("id", "name", "email", "phone", "created_at"),
            show="headings",
        )
        for col in ("id", "name", "email", "phone", "created_at"):
            self.student_tree.heading(col, text=col.capitalize())
            self.student_tree.column(col, width=120)
        self.student_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(
            list_frame, orient=tk.VERTICAL, command=self.student_tree.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.student_tree.configure(yscrollcommand=scrollbar.set)

        ttk.Button(
            list_frame, text="Delete Selected", command=self._delete_selected_student
        ).pack(pady=5)

        self._refresh_students()

    def _add_student(self):
        ok, msg = create_student(
            self.student_name_var.get(),
            self.student_email_var.get(),
            self.student_phone_var.get(),
        )
        messagebox.showinfo("Student", msg)
        if ok:
            self.student_name_var.set("")
            self.student_email_var.set("")
            self.student_phone_var.set("")
            self._refresh_students()

    def _refresh_students(self):
        for row in self.student_tree.get_children():
            self.student_tree.delete(row)
        for s in get_all_students():
            self.student_tree.insert(
                "", tk.END, values=(s["id"], s["name"], s["email"], s["phone"], s["created_at"])
            )

    def _delete_selected_student(self):
        selected = self.student_tree.selection()
        if not selected:
            messagebox.showwarning("Delete", "Please select a student.")
            return
        item = self.student_tree.item(selected[0])
        student_id = item["values"][0]
        delete_student(student_id)
        self._refresh_students()

    # -------------------------- COURSE TAB -------------------------- #
    def _build_course_tab(self):
        frm = self.course_frame

        form = ttk.LabelFrame(frm, text="Add Course")
        form.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(form, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(form, text="Code:").grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.course_name_var = tk.StringVar()
        self.course_code_var = tk.StringVar()

        ttk.Entry(form, textvariable=self.course_name_var, width=30).grid(
            row=0, column=1, padx=5, pady=5
        )
        ttk.Entry(form, textvariable=self.course_code_var, width=30).grid(
            row=1, column=1, padx=5, pady=5
        )

        ttk.Button(form, text="Add Course", command=self._add_course).grid(
            row=2, column=0, columnspan=2, pady=10
        )

        list_frame = ttk.LabelFrame(frm, text="Courses")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.course_tree = ttk.Treeview(
            list_frame, columns=("id", "name", "code"), show="headings"
        )
        for col in ("id", "name", "code"):
            self.course_tree.heading(col, text=col.capitalize())
            self.course_tree.column(col, width=150)
        self.course_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(
            list_frame, orient=tk.VERTICAL, command=self.course_tree.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.course_tree.configure(yscrollcommand=scrollbar.set)

        ttk.Button(
            list_frame, text="Delete Selected", command=self._delete_selected_course
        ).pack(pady=5)

        self._refresh_courses()

    def _add_course(self):
        ok, msg = create_course(self.course_name_var.get(), self.course_code_var.get())
        messagebox.showinfo("Course", msg)
        if ok:
            self.course_name_var.set("")
            self.course_code_var.set("")
            self._refresh_courses()

    def _refresh_courses(self):
        for row in self.course_tree.get_children():
            self.course_tree.delete(row)
        for c in get_all_courses():
            self.course_tree.insert("", tk.END, values=(c["id"], c["name"], c["code"]))

    def _delete_selected_course(self):
        selected = self.course_tree.selection()
        if not selected:
            messagebox.showwarning("Delete", "Please select a course.")
            return
        item = self.course_tree.item(selected[0])
        course_id = item["values"][0]
        delete_course(course_id)
        self._refresh_courses()

    # -------------------------- ATTENDANCE TAB -------------------------- #
    def _build_attendance_tab(self):
        frm = self.attendance_frame

        top = ttk.LabelFrame(frm, text="Select Course")
        top.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(top, text="Course:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.att_course_var = tk.StringVar()
        self.att_course_combo = ttk.Combobox(top, textvariable=self.att_course_var, state="readonly")
        self.att_course_combo.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(top, text="Refresh Courses", command=self._load_attendance_courses).grid(
            row=0, column=2, padx=5, pady=5
        )
        ttk.Button(top, text="Load Students", command=self._load_enrolled_students).grid(
            row=0, column=3, padx=5, pady=5
        )

        enroll_frame = ttk.LabelFrame(frm, text="Enroll Student to Course")
        enroll_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(enroll_frame, text="Student ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(enroll_frame, text="Course ID:").grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.enroll_student_id_var = tk.StringVar()
        self.enroll_course_id_var = tk.StringVar()

        ttk.Entry(enroll_frame, textvariable=self.enroll_student_id_var, width=10).grid(
            row=0, column=1, padx=5, pady=5
        )
        ttk.Entry(enroll_frame, textvariable=self.enroll_course_id_var, width=10).grid(
            row=1, column=1, padx=5, pady=5
        )

        ttk.Button(enroll_frame, text="Enroll", command=self._enroll_student_to_course).grid(
            row=2, column=0, columnspan=2, pady=5
        )

        mark_frame = ttk.LabelFrame(frm, text="Mark Attendance")
        mark_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(mark_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.att_date_var = tk.StringVar(value=today_str())
        ttk.Entry(mark_frame, textvariable=self.att_date_var, width=12).grid(
            row=0, column=1, padx=5, pady=5
        )

        ttk.Button(mark_frame, text="Mark Selected Present", command=lambda: self._mark_selected("Present")).grid(
            row=0, column=2, padx=5, pady=5
        )
        ttk.Button(mark_frame, text="Mark Selected Absent", command=lambda: self._mark_selected("Absent")).grid(
            row=0, column=3, padx=5, pady=5
        )

        list_frame = ttk.LabelFrame(frm, text="Enrolled Students")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.att_tree = ttk.Treeview(
            list_frame,
            columns=("student_id", "name", "email"),
            show="headings",
            selectmode="extended",
        )
        for col in ("student_id", "name", "email"):
            self.att_tree.heading(col, text=col.capitalize())
            self.att_tree.column(col, width=150)
        self.att_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.att_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.att_tree.configure(yscrollcommand=scrollbar.set)

        self._load_attendance_courses()

    def _load_attendance_courses(self):
        courses = get_all_courses()
        display = [f'{c["id"]} - {c["name"]} ({c["code"]})' for c in courses]
        self.att_course_combo["values"] = display

    def _get_selected_course_id(self) -> int | None:
        val = self.att_course_var.get()
        if not val:
            return None
        try:
            return int(val.split(" - ")[0])
        except ValueError:
            return None

    def _load_enrolled_students(self):
        course_id = self._get_selected_course_id()
        if not course_id:
            messagebox.showwarning("Attendance", "Please select a course.")
            return
        for row in self.att_tree.get_children():
            self.att_tree.delete(row)
        for s in get_enrolled_students(course_id):
            self.att_tree.insert("", tk.END, values=(s["id"], s["name"], s["email"]))

    def _enroll_student_to_course(self):
        try:
            student_id = int(self.enroll_student_id_var.get())
            course_id = int(self.enroll_course_id_var.get())
        except ValueError:
            messagebox.showerror("Enroll", "Student ID and Course ID must be numbers.")
            return

        ok, msg = enroll_student(student_id, course_id)
        messagebox.showinfo("Enroll", msg)

    def _mark_selected(self, status: str):
        course_id = self._get_selected_course_id()
        if not course_id:
            messagebox.showwarning("Attendance", "Please select a course.")
            return

        date_str = self.att_date_var.get().strip()
        selected_items = self.att_tree.selection()
        if not selected_items:
            messagebox.showwarning("Attendance", "Please select at least one student.")
            return

        for item_id in selected_items:
            item = self.att_tree.item(item_id)
            student_id = int(item["values"][0])
            ok, msg = mark_attendance(student_id, course_id, status, date_str)
            if not ok:
                messagebox.showerror("Attendance", msg)
                return

        messagebox.showinfo("Attendance", f"{status} marked for selected students.")

    # -------------------------- REPORT TAB -------------------------- #
    def _build_report_tab(self):
        frm = self.report_frame

        top = ttk.LabelFrame(frm, text="Select Course")
        top.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(top, text="Course:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.rep_course_var = tk.StringVar()
        self.rep_course_combo = ttk.Combobox(top, textvariable=self.rep_course_var, state="readonly")
        self.rep_course_combo.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(top, text="Refresh Courses", command=self._load_report_courses).grid(
            row=0, column=2, padx=5, pady=5
        )
        ttk.Button(top, text="Load Summary", command=self._load_report_summary).grid(
            row=0, column=3, padx=5, pady=5
        )

        list_frame = ttk.LabelFrame(frm, text="Attendance Summary")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.rep_tree = ttk.Treeview(
            list_frame,
            columns=("name", "present", "absent", "total", "percentage"),
            show="headings",
        )
        headers = {
            "name": "Student Name",
            "present": "Present",
            "absent": "Absent",
            "total": "Total",
            "percentage": "% Present",
        }
        for col, text in headers.items():
            self.rep_tree.heading(col, text=text)
            self.rep_tree.column(col, width=120)
        self.rep_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.rep_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.rep_tree.configure(yscrollcommand=scrollbar.set)

        self._load_report_courses()

    def _load_report_courses(self):
        courses = get_all_courses()
        display = [f'{c["id"]} - {c["name"]} ({c["code"]})' for c in courses]
        self.rep_course_combo["values"] = display

    def _get_report_course_id(self) -> int | None:
        val = self.rep_course_var.get()
        if not val:
            return None
        try:
            return int(val.split(" - ")[0])
        except ValueError:
            return None

    def _load_report_summary(self):
        course_id = self._get_report_course_id()
        if not course_id:
            messagebox.showwarning("Report", "Please select a course.")
            return
        for row in self.rep_tree.get_children():
            self.rep_tree.delete(row)
        data = attendance_summary_by_course(course_id)
        for d in data:
            self.rep_tree.insert(
                "",
                tk.END,
                values=(
                    d["student_name"],
                    d["present_count"],
                    d["absent_count"],
                    d["total"],
                    d["percentage"],
                ),
            )


def run_app():
    app = StudentAttendanceApp()
    app.mainloop()
