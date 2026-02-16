"""
Student & Teacher Info — desktop application.
Run: python gui.py  (or double-click the built .exe)
"""
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import sys
import os

# Developer mode: set environment variable BYPASS_AUTH=1 to skip login
DEV_MODE = os.environ.get("BYPASS_AUTH", "").strip() in ("1", "true", "True", "TRUE", "yes", "Yes", "YES")

# Application root: folder containing this script, or the executable when built
if getattr(sys, "frozen", False):
    APP_DIR = os.path.dirname(sys.executable)
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

import auth
from student import Student
from teacher import Teacher
from InfoManager import InfoManager

# Data files live next to the app (or exe)
auth.USERS_FILE = os.path.join(APP_DIR, "users.txt")
InfoManager.studentfile = os.path.join(APP_DIR, "student.txt")
InfoManager.teacherfile = os.path.join(APP_DIR, "teacher.txt")


# Gender choices (stored in title case)
GENDERS = ["Male", "Female", "Other"]

# Futuristic theme
BG = "#060810"
SURFACE = "#0d1321"
CARD = "#131b2e"
ACCENT = "#00d4ff"
ACCENT_DIM = "#0099bb"
TEXT = "#e6edf3"
TEXT_MUTED = "#8b949e"
BORDER = "#21262d"
GLOW = "#00d4ff"
FONT = ("Segoe UI", 10)
FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_MONO = ("Consolas", 10)
PAD = 10


def _setup_futuristic_theme(root):
    root.configure(bg=BG)
    root.option_add("*Background", BG)
    root.option_add("*Foreground", TEXT)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(".", background=SURFACE, foreground=TEXT, fieldbackground=CARD)
    style.configure("TFrame", background=SURFACE)
    style.configure("TLabel", background=SURFACE, foreground=TEXT, font=FONT)
    style.configure("TLabelframe", background=SURFACE, foreground=ACCENT)
    style.configure("TLabelframe.Label", background=SURFACE, foreground=ACCENT, font=("Segoe UI", 11, "bold"))
    style.configure("TButton", background=CARD, foreground=TEXT, font=FONT, padding=(12, 6))
    style.map("TButton", background=[("active", ACCENT_DIM), ("pressed", ACCENT)], foreground=[("active", BG)])
    style.configure("TEntry", fieldbackground=CARD, foreground=TEXT, insertcolor=ACCENT)
    style.configure("TCombobox", fieldbackground=CARD, foreground=TEXT, background=SURFACE)
    style.map("TCombobox", fieldbackground=[("readonly", CARD)], background=[("readonly", SURFACE)])
    style.configure("TRadiobutton", background=SURFACE, foreground=TEXT_MUTED)
    style.map("TRadiobutton", foreground=[("active", ACCENT)])
    style.configure("Vertical.TScrollbar", background=SURFACE, troughcolor=CARD)
    style.configure("Horizontal.TScrollbar", background=SURFACE, troughcolor=CARD)
    style.configure("Muted.TLabel", background=SURFACE, foreground=TEXT_MUTED)
    style.configure("Card.TFrame", background=CARD)
    style.configure("Card.TLabel", background=CARD, foreground=TEXT)
    style.configure("Accent.TLabel", background=SURFACE, foreground=ACCENT)


def _format_teacher(t):
    return (
        f"Name: {t._name}\n"
        f"Age: {t._age}  |  Gender: {t._gender}  |  ID: {t._id}\n"
        f"Subject: {t._subject}  |  Salary: ${t._salary}\n"
    )


def _format_student(s):
    return (
        f"Name: {s._name}\n"
        f"Age: {s._age}  |  Gender: {s._gender}  |  ID: {s._id}\n"
        f"Major: {s._major}\n"
    )


class LoginFrame(ttk.Frame):
    def __init__(self, parent, on_success, on_show_signup, **kwargs):
        super().__init__(parent, **kwargs)
        self.on_success = on_success
        self.on_show_signup = on_show_signup
        self.setup_ui()
        # Developer bypass: Ctrl+Shift+D to skip login
        self.bind_all("<Control-Shift-D>", lambda e: self.dev_bypass())
        self.bind_all("<Control-Shift-d>", lambda e: self.dev_bypass())

    def setup_ui(self):
        # Card with neon border
        card_outer = tk.Frame(self, bg=ACCENT, padx=2, pady=2)
        card_outer.place(relx=0.5, rely=0.5, anchor="center")
        card = tk.Frame(card_outer, bg=CARD, padx=44, pady=36)
        card.pack()
        inner = ttk.Frame(card, padding=0, style="Card.TFrame")
        inner.pack()

        ttk.Label(inner, text="STUDENT & TEACHER INFO", font=FONT_TITLE, style="Card.TLabel").grid(row=0, column=0, columnspan=2, pady=(0, 6))
        msg = "Sign in or create an account to continue."
        if DEV_MODE:
            msg += " [DEV MODE: Auth bypassed]"
        ttk.Label(inner, text=msg, style="Card.TLabel", foreground=TEXT_MUTED).grid(row=1, column=0, columnspan=2, pady=(0, 20))
        if not DEV_MODE:
            ttk.Label(inner, text="(Dev bypass: Ctrl+Shift+D)", style="Card.TLabel", foreground=TEXT_MUTED, font=("Segoe UI", 8)).grid(row=8, column=0, columnspan=2, pady=(10, 0))

        ttk.Label(inner, text="Username:", style="Card.TLabel").grid(row=2, column=0, sticky="e", padx=(0, PAD), pady=PAD)
        self.username = ttk.Entry(inner, width=26)
        self.username.grid(row=2, column=1, pady=PAD)
        self.username.focus()

        ttk.Label(inner, text="Password:", style="Card.TLabel").grid(row=3, column=0, sticky="e", padx=(0, PAD), pady=PAD)
        self.password = ttk.Entry(inner, width=26, show="•")
        self.password.grid(row=3, column=1, pady=PAD)
        self.password.bind("<Return>", lambda e: self.do_login())

        btn_frame = ttk.Frame(inner)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text="Log in", command=self.do_login).pack(side="left", padx=(0, PAD))
        ttk.Button(btn_frame, text="Create account", command=self.do_create).pack(side="left")

    def do_login(self):
        u, p = self.username.get().strip(), self.password.get()
        if not u:
            messagebox.showwarning("Missing field", "Please enter a username.")
            return
        if auth.login(u, p):
            self.on_success()
            return
        messagebox.showerror("Login failed", "Invalid username or password.")

    def do_create(self):
        self.on_show_signup()
    
    def dev_bypass(self):
        """Developer bypass: skip authentication."""
        messagebox.showinfo("Developer Mode", "Authentication bypassed for development.")
        self.on_success()


class SignUpFrame(ttk.Frame):
    """Sign-up form: first name, last name, phone, DOB, country, zipcode, address, username, password."""
    def __init__(self, parent, on_back, on_success, **kwargs):
        super().__init__(parent, **kwargs)
        self.on_back = on_back
        self.on_success = on_success
        self.setup_ui()

    def setup_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        canvas = tk.Canvas(self, highlightthickness=0, bg=SURFACE)
        scroll = ttk.Scrollbar(self)
        inner = ttk.Frame(canvas, padding=24)
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)
        scroll.config(command=canvas.yview)
        canvas.grid(row=0, column=0, sticky="nswe")
        scroll.grid(row=0, column=1, sticky="ns")
        inner.columnconfigure(1, weight=1)

        ttk.Label(inner, text="CREATE ACCOUNT", font=FONT_TITLE, style="Accent.TLabel").grid(row=0, column=0, columnspan=2, pady=(0, 16))
        ttk.Label(inner, text="Please fill in your information.", style="Muted.TLabel").grid(row=1, column=0, columnspan=2, pady=(0, 16))

        row = 2
        self.first_name = ttk.Entry(inner, width=32)
        self._row(inner, "First name", row, self.first_name)
        row += 1
        self.last_name = ttk.Entry(inner, width=32)
        self._row(inner, "Last name", row, self.last_name)
        row += 1
        self.phone = ttk.Entry(inner, width=32)
        self._row(inner, "Phone number", row, self.phone)
        row += 1
        self.dob = ttk.Entry(inner, width=32)
        self._row(inner, "Date of birth (e.g. YYYY-MM-DD)", row, self.dob)
        row += 1
        self.country = ttk.Entry(inner, width=32)
        self._row(inner, "Country", row, self.country)
        row += 1
        self.zipcode = ttk.Entry(inner, width=32)
        self._row(inner, "Zipcode", row, self.zipcode)
        row += 1
        self.address = ScrolledText(inner, height=3, width=32, wrap=tk.WORD, bg=CARD, fg=TEXT, insertbackground=ACCENT, font=FONT_MONO)
        ttk.Label(inner, text="Address:").grid(row=row, column=0, sticky="ne", padx=(0, PAD), pady=PAD)
        self.address.grid(row=row, column=1, sticky="ew", pady=PAD)
        row += 1
        self.username = ttk.Entry(inner, width=32)
        self._row(inner, "Username", row, self.username)
        row += 1
        self.password = ttk.Entry(inner, width=32, show="•")
        self._row(inner, "Password", row, self.password)
        row += 1
        self.confirm = ttk.Entry(inner, width=32, show="•")
        self._row(inner, "Confirm password", row, self.confirm)
        row += 1

        btn_frame = ttk.Frame(inner)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text="Back to login", command=self.on_back).pack(side="left", padx=(0, PAD))
        ttk.Button(btn_frame, text="Sign up", command=self.do_signup).pack(side="left")

    def _row(self, parent, label, row, widget):
        ttk.Label(parent, text=label + ":", width=28, anchor="e").grid(row=row, column=0, sticky="e", padx=(0, PAD), pady=PAD)
        widget.grid(row=row, column=1, sticky="ew", pady=PAD)

    def do_signup(self):
        first = self.first_name.get().strip()
        last = self.last_name.get().strip()
        phone = self.phone.get().strip()
        dob = self.dob.get().strip()
        country = self.country.get().strip()
        zipcode = self.zipcode.get().strip()
        address = self.address.get("1.0", tk.END).strip()
        u = self.username.get().strip()
        p = self.password.get()
        p2 = self.confirm.get()

        if not first:
            messagebox.showwarning("Missing field", "Please enter your first name.")
            return
        if not last:
            messagebox.showwarning("Missing field", "Please enter your last name.")
            return
        if not phone:
            messagebox.showwarning("Missing field", "Please enter your phone number.")
            return
        if not dob:
            messagebox.showwarning("Missing field", "Please enter your date of birth.")
            return
        if not country:
            messagebox.showwarning("Missing field", "Please enter your country.")
            return
        if not zipcode:
            messagebox.showwarning("Missing field", "Please enter your zipcode.")
            return
        if not address:
            messagebox.showwarning("Missing field", "Please enter your address.")
            return
        if not u:
            messagebox.showwarning("Missing field", "Please choose a username.")
            return
        if not p:
            messagebox.showwarning("Missing field", "Please enter a password.")
            return
        if p != p2:
            messagebox.showwarning("Password mismatch", "Password and Confirm password do not match.")
            return

        if auth.create_account(u, p, first_name=first, last_name=last, phone=phone, date_of_birth=dob, country=country, zipcode=zipcode, address=address):
            messagebox.showinfo("Account created", "Your account has been created. You can log in now.")
            self.on_success()
            return
        messagebox.showerror("Cannot create account", "That username is already taken.")


class FormMixin:
    """Shared helpers for add teacher/student forms."""
    def make_row(self, parent, label, row, entry_var=None, widget=None):
        ttk.Label(parent, text=label + ":", width=12, anchor="e").grid(row=row, column=0, sticky="ew", padx=(0, PAD), pady=PAD)
        if widget is not None:
            widget.grid(row=row, column=1, sticky="ew", pady=PAD)
            return widget
        e = ttk.Entry(parent, textvariable=entry_var, width=30)
        e.grid(row=row, column=1, sticky="ew", pady=PAD)
        return e

    def get_gender(self, var):
        return var.get().strip() or None


class AddTeacherForm(ttk.Frame, FormMixin):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.setup_ui()

    def setup_ui(self):
        form = ttk.LabelFrame(self, text="Add a new teacher", padding=PAD)
        form.pack(fill="both", expand=True, padx=PAD, pady=PAD)
        form.columnconfigure(1, weight=1)

        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.gender_var = tk.StringVar()
        self.id_var = tk.StringVar()
        self.subject_var = tk.StringVar()
        self.salary_var = tk.StringVar()

        self.make_row(form, "Name", 0, self.name_var)
        self.make_row(form, "Age", 1, self.age_var)
        self.gender_cb = ttk.Combobox(form, textvariable=self.gender_var, values=GENDERS, width=28, state="readonly")
        self.make_row(form, "Gender", 2, widget=self.gender_cb)
        self.make_row(form, "ID", 3, self.id_var)
        self.make_row(form, "Subject", 4, self.subject_var)
        self.make_row(form, "Salary", 5, self.salary_var)

        ttk.Button(form, text="Save teacher", command=self.submit).grid(row=6, column=0, columnspan=2, pady=(PAD * 2, 0))

    def submit(self):
        try:
            t = Teacher(
                self.name_var.get().strip() or None,
                self.age_var.get().strip() or None,
                self.get_gender(self.gender_var),
                self.id_var.get().strip() or None,
                self.subject_var.get().strip() or None,
                self.salary_var.get().strip() or None,
            )
            t.name = t._name
            t.age = t._age
            t.gender = t._gender
            t.id = t._id
            t.subject = t._subject
            t.salary = t._salary
            InfoManager.add_teacher(t)
            messagebox.showinfo("Success", "Teacher added successfully.")
            self.clear()
        except (ValueError, AttributeError, TypeError) as e:
            messagebox.showerror("Invalid input", str(e))

    def clear(self):
        for v in (self.name_var, self.age_var, self.gender_var, self.id_var, self.subject_var, self.salary_var):
            v.set("")


class AddStudentForm(ttk.Frame, FormMixin):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.setup_ui()

    def setup_ui(self):
        form = ttk.LabelFrame(self, text="Add a new student", padding=PAD)
        form.pack(fill="both", expand=True, padx=PAD, pady=PAD)
        form.columnconfigure(1, weight=1)

        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.gender_var = tk.StringVar()
        self.id_var = tk.StringVar()
        self.major_var = tk.StringVar()

        self.make_row(form, "Name", 0, self.name_var)
        self.make_row(form, "Age", 1, self.age_var)
        self.gender_cb = ttk.Combobox(form, textvariable=self.gender_var, values=GENDERS, width=28, state="readonly")
        self.make_row(form, "Gender", 2, widget=self.gender_cb)
        self.make_row(form, "ID", 3, self.id_var)
        self.make_row(form, "Major", 4, self.major_var)

        ttk.Button(form, text="Save student", command=self.submit).grid(row=5, column=0, columnspan=2, pady=(PAD * 2, 0))

    def submit(self):
        try:
            s = Student(
                self.name_var.get().strip() or None,
                self.age_var.get().strip() or None,
                self.get_gender(self.gender_var),
                self.id_var.get().strip() or None,
                self.major_var.get().strip() or None,
            )
            s.name = s._name
            s.age = s._age
            s.gender = s._gender
            s.id = s._id
            s.major = s._major
            InfoManager.add_student(s)
            messagebox.showinfo("Success", "Student added successfully.")
            self.clear()
        except (ValueError, AttributeError, TypeError) as e:
            messagebox.showerror("Invalid input", str(e))

    def clear(self):
        for v in (self.name_var, self.age_var, self.gender_var, self.id_var, self.major_var):
            v.set("")


class LookupTeacherFrame(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.setup_ui()

    def setup_ui(self):
        top = ttk.Frame(self)
        top.pack(fill="x", padx=PAD, pady=PAD)
        self.search_var = tk.StringVar()
        self.by_id = tk.BooleanVar(value=True)
        ttk.Radiobutton(top, text="Search by ID", variable=self.by_id, value=True).pack(side="left", padx=(0, 12))
        ttk.Radiobutton(top, text="Search by name", variable=self.by_id, value=False).pack(side="left", padx=(0, 12))
        ttk.Entry(top, textvariable=self.search_var, width=25).pack(side="left", padx=(0, PAD))
        ttk.Button(top, text="Search", command=self.search).pack(side="left")

        self.result = ScrolledText(self, wrap=tk.WORD, height=15, font=FONT_MONO, bg=CARD, fg=TEXT, insertbackground=ACCENT)
        self.result.pack(fill="both", expand=True, padx=PAD, pady=(0, PAD))

    def search(self):
        self.result.delete("1.0", tk.END)
        key = self.search_var.get().strip()
        if not key:
            self.result.insert(tk.END, "Enter an ID or name and click Search.")
            return
        if self.by_id.get():
            t = InfoManager.lookup_teacher_by_id(key)
            if t:
                self.result.insert(tk.END, _format_teacher(t))
            else:
                self.result.insert(tk.END, "No teacher found with that ID.")
        else:
            teachers = InfoManager.lookup_teacher_by_name(key)
            if teachers:
                for t in teachers:
                    self.result.insert(tk.END, _format_teacher(t) + "\n")
            else:
                self.result.insert(tk.END, "No teachers found with that name.")


class LookupStudentFrame(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.setup_ui()

    def setup_ui(self):
        top = ttk.Frame(self)
        top.pack(fill="x", padx=PAD, pady=PAD)
        self.search_var = tk.StringVar()
        self.by_id = tk.BooleanVar(value=True)
        ttk.Radiobutton(top, text="Search by ID", variable=self.by_id, value=True).pack(side="left", padx=(0, 12))
        ttk.Radiobutton(top, text="Search by name", variable=self.by_id, value=False).pack(side="left", padx=(0, 12))
        ttk.Entry(top, textvariable=self.search_var, width=25).pack(side="left", padx=(0, PAD))
        ttk.Button(top, text="Search", command=self.search).pack(side="left")

        self.result = ScrolledText(self, wrap=tk.WORD, height=15, font=FONT_MONO, bg=CARD, fg=TEXT, insertbackground=ACCENT)
        self.result.pack(fill="both", expand=True, padx=PAD, pady=(0, PAD))

    def search(self):
        self.result.delete("1.0", tk.END)
        key = self.search_var.get().strip()
        if not key:
            self.result.insert(tk.END, "Enter an ID or name and click Search.")
            return
        if self.by_id.get():
            s = InfoManager.lookup_student_by_id(key)
            if s:
                self.result.insert(tk.END, _format_student(s))
            else:
                self.result.insert(tk.END, "No student found with that ID.")
        else:
            students = InfoManager.lookup_student_by_name(key)
            if students:
                for s in students:
                    self.result.insert(tk.END, _format_student(s) + "\n")
            else:
                self.result.insert(tk.END, "No students found with that name.")


class ListTeachersFrame(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.text = ScrolledText(self, wrap=tk.WORD, font=FONT_MONO, bg=CARD, fg=TEXT, insertbackground=ACCENT)
        self.text.pack(fill="both", expand=True, padx=PAD, pady=PAD)
        ttk.Button(self, text="Refresh list", command=self.refresh).pack(anchor="w", padx=PAD, pady=(0, PAD))

    def refresh(self):
        self.text.delete("1.0", tk.END)
        teachers = InfoManager.load_teachers()
        if not teachers:
            self.text.insert(tk.END, "No teachers on file.")
            return
        self.text.insert(tk.END, f"Total: {len(teachers)} teacher(s)\n\n")
        for t in teachers:
            self.text.insert(tk.END, _format_teacher(t) + "\n")


class ListStudentsFrame(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.text = ScrolledText(self, wrap=tk.WORD, font=FONT_MONO, bg=CARD, fg=TEXT, insertbackground=ACCENT)
        self.text.pack(fill="both", expand=True, padx=PAD, pady=PAD)
        ttk.Button(self, text="Refresh list", command=self.refresh).pack(anchor="w", padx=PAD, pady=(0, PAD))

    def refresh(self):
        self.text.delete("1.0", tk.END)
        students = InfoManager.load_students()
        if not students:
            self.text.insert(tk.END, "No students on file.")
            return
        self.text.insert(tk.END, f"Total: {len(students)} student(s)\n\n")
        for s in students:
            self.text.insert(tk.END, _format_student(s) + "\n")


class MainFrame(ttk.Frame):
    def __init__(self, parent, on_logout, **kwargs):
        super().__init__(parent, **kwargs)
        self.on_logout = on_logout
        self.views = {}
        self.setup_ui()

    def setup_ui(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # Sidebar
        sidebar = ttk.Frame(self, padding=PAD)
        sidebar.grid(row=0, column=0, sticky="nswe")
        ttk.Label(sidebar, text="STUDENT & TEACHER INFO", font=FONT_TITLE, style="Accent.TLabel").pack(anchor="w", pady=(0, 16))

        nav = [
            ("Add teacher", self.show_add_teacher),
            ("Add student", self.show_add_student),
            ("Look up teacher", self.show_lookup_teacher),
            ("Look up student", self.show_lookup_student),
            ("List all teachers", self.show_list_teachers),
            ("List all students", self.show_list_students),
        ]
        for label, cmd in nav:
            ttk.Button(sidebar, text=label, command=cmd).pack(fill="x", pady=2)

        ttk.Separator(sidebar, orient="horizontal").pack(fill="x", pady=12)
        ttk.Button(sidebar, text="Log out", command=self.on_logout).pack(fill="x")

        # Content area
        self.content = ttk.Frame(self, padding=PAD)
        self.content.grid(row=0, column=1, sticky="nswe")
        self.content.columnconfigure(0, weight=1)
        self.content.rowconfigure(0, weight=1)

        self.views["add_teacher"] = AddTeacherForm(self.content)
        self.views["add_student"] = AddStudentForm(self.content)
        self.views["lookup_teacher"] = LookupTeacherFrame(self.content)
        self.views["lookup_student"] = LookupStudentFrame(self.content)
        self.views["list_teachers"] = ListTeachersFrame(self.content)
        self.views["list_students"] = ListStudentsFrame(self.content)

        self.show_add_teacher()

    def show(self, name):
        for k, v in self.views.items():
            if k == name:
                v.grid(row=0, column=0, sticky="nswe")
            else:
                v.grid_remove()
        if name == "list_teachers":
            self.views["list_teachers"].refresh()
        elif name == "list_students":
            self.views["list_students"].refresh()

    def show_add_teacher(self):
        self.show("add_teacher")

    def show_add_student(self):
        self.show("add_student")

    def show_lookup_teacher(self):
        self.show("lookup_teacher")

    def show_lookup_student(self):
        self.show("lookup_student")

    def show_list_teachers(self):
        self.show("list_teachers")

    def show_list_students(self):
        self.show("list_students")


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Student & Teacher Info")
        self.root.minsize(700, 480)
        self.root.geometry("820x520")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        _setup_futuristic_theme(self.root)

        self.container = ttk.Frame(self.root, padding=10)
        self.container.grid(row=0, column=0, sticky="nswe")
        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(0, weight=1)

        self.login_frame = LoginFrame(self.container, on_success=self.show_main, on_show_signup=self.show_signup)
        self.signup_frame = SignUpFrame(self.container, on_back=self.show_login, on_success=self.show_login)
        self.main_frame = MainFrame(self.container, on_logout=self.show_login)
        
        # If developer mode is enabled via environment variable, skip login
        if DEV_MODE:
            self.show_main()
        else:
            self.show_login()

    def show_login(self):
        self.main_frame.grid_remove()
        self.signup_frame.grid_remove()
        self.login_frame.grid(row=0, column=0, sticky="nswe")

    def show_signup(self):
        self.main_frame.grid_remove()
        self.login_frame.grid_remove()
        self.signup_frame.grid(row=0, column=0, sticky="nswe")

    def show_main(self):
        self.login_frame.grid_remove()
        self.signup_frame.grid_remove()
        self.main_frame.grid(row=0, column=0, sticky="nswe")

    def run(self):
        self.root.mainloop()


def main():
    app = App()
    app.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Student & Teacher Info", f"An error occurred:\n\n{e}")
        if not getattr(sys, "frozen", False):
            raise
