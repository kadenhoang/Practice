from student import Student
from teacher import Teacher

class InfoManager:
    studentfile = "student.txt"
    teacherfile = "teacher.txt"

    @classmethod
    def save_student(cls, student):
        # PSEUDOCODE: Open student file in append mode, write one line (name,age,gender,id,major), close file
        with open(cls.studentfile, "a") as file:
            file.write(f"{student._name},{student._age},{student._gender},{student._id},{student._major}\n")

    @classmethod
    def save_teacher(cls, teacher):
        # PSEUDOCODE: Open teacher file in append mode, write one line (name,age,gender,id,subject,salary), close file
        with open(cls.teacherfile, "a") as file:
            file.write(f"{teacher._name},{teacher._age},{teacher._gender},{teacher._id},{teacher._subject},{teacher._salary}\n")
    
    @classmethod
    def add_student(cls, student=None):
        # PSEUDOCODE: IF no student given THEN get student via prompt (Student.get_student), save student to file, print success
        if student is None:
            student = Student.get_student()
        cls.save_student(student)

    @classmethod
    def add_teacher(cls, teacher=None):
        # PSEUDOCODE: IF no teacher given THEN get teacher via prompt (Teacher.get_teacher), save teacher to file, print success
        if teacher is None:
            teacher = Teacher.get_teacher()
        cls.save_teacher(teacher)

    @classmethod
    def lookup_student_by_id(cls, id):
        # PSEUDOCODE: Load all students, FOR each student IF student.id equals given id THEN return student, RETURN None if no match
        students = cls.load_students()
        for s in students:
            if s._id == str(id):
                return s
        return None

    @classmethod
    def lookup_student_by_name(cls, name):
        # PSEUDOCODE: Load all students, RETURN list of students whose name (case-insensitive) contains the given name
        students = cls.load_students()
        return [s for s in students if name.lower() in (s._name or "").lower()]

    @classmethod
    def lookup_teacher_by_id(cls, id):
        # PSEUDOCODE: Load all teachers, FOR each teacher IF teacher.id equals given id THEN return teacher, RETURN None if no match
        teachers = cls.load_teachers()
        for t in teachers:
            if t._id == str(id):
                return t
        return None

    @classmethod
    def lookup_teacher_by_name(cls, name):
        # PSEUDOCODE: Load all teachers, RETURN list of teachers whose name (case-insensitive) contains the given name
        teachers = cls.load_teachers()
        return [t for t in teachers if name.lower() in (t._name or "").lower()]

    @classmethod
    def load_students(cls):
        # PSEUDOCODE: Create empty list, open student file (IF not found print message, return empty list), FOR each line parse (name,age,gender,id,major), create Student, append to list, RETURN list
        students = []
        try:
            with open(cls.studentfile, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        name, age, gender, id, major = line.split(",")
                        students.append(Student(name, age, gender, id, major))
                    except (ValueError, TypeError) as e:
                        print(f"Skipping invalid student line: {e}")
        except FileNotFoundError:
            print("No student information available.")
        return students

    @classmethod
    def load_teachers(cls):
        # PSEUDOCODE: Create empty list, open teacher file (IF not found print message, return empty list), FOR each line parse (name,age,gender,id,subject,salary), create Teacher, append to list, RETURN list
        teachers = []
        try:
            with open(cls.teacherfile, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        name, age, gender, id, subject, salary = line.split(",")
                        teachers.append(Teacher(name, age, gender, id, subject, salary))
                    except (ValueError, TypeError) as e:
                        print(f"Skipping invalid teacher line: {e}")
        except FileNotFoundError:
            print("No teacher information available.")
        return teachers 