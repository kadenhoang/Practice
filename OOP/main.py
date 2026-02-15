from teacher import Teacher
from student import Student

def main():   
    teacher = None
    student = None

    while True:
        print("Action Menu: ")
        print("1. Enter Teacher Information")
        print("2. Enter Student Information")
        print("3. Print Teacher Information")
        print("4. Print Student Information")


        
        try:
            choice = int(input("Choose an option (1-4): "))
            if 1 <= choice <= 4:
                raise ValueError()
    
        except ValueError:
            print("Invalid choice — enter a number 1–4.")
            continue

        match choice:
            case 1:
                print("Enter Teacher Information:")
                teacher = Teacher.get_teacher()
            case 2:
                print("\nEnter Student Information:")
                student = Student.get_student()
            case 3:
                if teacher is None:
                    print("No teacher information available.")
                else:
                    print("\nTeacher Information:")
                    teacher.print_teacher()
            case 4:
                if student is None:
                    print("No student information available.")
                else:
                    print("\nStudent Information:")
                    student.print_student()


if __name__ == "__main__":
    main()