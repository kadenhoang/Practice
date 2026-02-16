from teacher import Teacher
from student import Student
from InfoManager import InfoManager
from auth import require_auth
from ui import (
    title,
    section,
    prompt,
    menu,
    success,
    error,
    info,
    card_title,
    wait_to_continue,
    goodbye_banner,
)


def main():
    """
    PSEUDOCODE (Main):
      Require user to login or create account (require_auth); then
      REPEAT main menu (Add/Lookup/List Teacher/Student, Exit) until Exit
    """
    require_auth()

    main_options = [
        "Add a teacher",
        "Add a student",
        "Look up a teacher (by ID or name)",
        "Look up a student (by ID or name)",
        "List all teachers",
        "List all students",
        "Exit",
    ]

    while True:
        title("What would you like to do?")
        choice = menu(
            main_options,
            title_text="Your choice",
            hint="Enter the number of the action you want.",
        )

        if not choice or choice not in "1234567":
            error("Please enter a number from 1 to 7.")
            continue

        if choice == "7":
            goodbye_banner()
            break

        if choice == "1":
            section("Add a new teacher")
            info("Enter the teacher's details below. All fields are required.")
            teacher = Teacher.get_teacher()
            InfoManager.add_teacher(teacher)
            success("Teacher added successfully.")
            wait_to_continue()

        elif choice == "2":
            section("Add a new student")
            info("Enter the student's details below. All fields are required.")
            student = Student.get_student()
            InfoManager.add_student(student)
            success("Student added successfully.")
            wait_to_continue()

        elif choice == "3":
            section("Look up a teacher")
            lookup = menu(
                ["Search by ID", "Search by name (or part of name)"],
                title_text="How do you want to search",
                hint="Enter 1 for ID, 2 for name.",
            )
            if lookup == "1":
                tid = prompt("Teacher ID: ")
                t = InfoManager.lookup_teacher_by_id(tid)
                if t:
                    card_title("Teacher information")
                    t.print_teacher()
                else:
                    error("No teacher found with that ID.")
            else:
                name = prompt("Teacher name (or part of it): ")
                teachers = InfoManager.lookup_teacher_by_name(name)
                if teachers:
                    for t in teachers:
                        card_title("Teacher information")
                        t.print_teacher()
                        print()
                else:
                    error("No teachers found with that name.")
            wait_to_continue()

        elif choice == "4":
            section("Look up a student")
            lookup = menu(
                ["Search by ID", "Search by name (or part of name)"],
                title_text="How do you want to search",
                hint="Enter 1 for ID, 2 for name.",
            )
            if lookup == "1":
                sid = prompt("Student ID: ")
                s = InfoManager.lookup_student_by_id(sid)
                if s:
                    card_title("Student information")
                    s.print_student()
                else:
                    error("No student found with that ID.")
            else:
                name = prompt("Student name (or part of it): ")
                students = InfoManager.lookup_student_by_name(name)
                if students:
                    for s in students:
                        card_title("Student information")
                        s.print_student()
                        print()
                else:
                    error("No students found with that name.")
            wait_to_continue()

        elif choice == "5":
            section("All teachers")
            teachers = InfoManager.load_teachers()
            if not teachers:
                info("No teachers on file yet.")
            else:
                info(f"Found {len(teachers)} teacher(s).")
                print()
                for t in teachers:
                    card_title("Teacher")
                    t.print_teacher()
                    print()
            wait_to_continue()

        elif choice == "6":
            section("All students")
            students = InfoManager.load_students()
            if not students:
                info("No students on file yet.")
            else:
                info(f"Found {len(students)} student(s).")
                print()
                for s in students:
                    card_title("Student")
                    s.print_student()
                    print()
            wait_to_continue()


if __name__ == "__main__":
    main()
