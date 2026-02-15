from student import Student
from teacher import Teacher

class InfoManager:
    studentfile = "student.txt"
    teacherfile = "teacher.txt"

    @classmethod
    def save_student(cls, student):
        with open(cls.studentfile, "a") as file:
            file.write(f"{student._name},{student._age},{student._gender},{student._id},{student._major}\n")

    @classmethod
    def save_teacher(cls, teacher):
        with open(cls.teacherfile, "a") as file:
            file.write(f"{teacher._name},{teacher._age},{teacher._gender},{teacher._id},{teacher._subject},{teacher._salary}\n")
    
    @classmethod
    def add_student(cls, student):
        student = Student.get_student()
        cls.save_student(student)
        print("Student added successfully.")

    @classmethod
    def add_teacher(cls, teacher):
        teacher = Teacher.get_teacher()
        cls.save_teacher(teacher)
        print("Teacher added successfully.")    

    @classmethod
    def load_students(cls):
        students = []
        try:
            with open(cls.studentfile, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    name, age, gender, id, major = line.split(",")
                    students.append(Student(name, age, gender, id, major))
        except FileNotFoundError:
            print("No student information available.")
        return students

    @classmethod
    def load_teachers(cls):
        teachers = []
        try:
            with open(cls.teacherfile, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    name, age, gender, id, subject, salary = line.split(",")
                    teachers.append(Teacher(name, age, gender, id, subject, salary))
        except FileNotFoundError:
            print("No teacher information available.")
        return teachers 