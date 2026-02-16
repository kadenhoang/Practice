from human import Human, required_input
import string

class Teacher(Human):
    
    def __init__(self, name = None, age = None, gender = None, id = None, subject = None, salary = None):
        super().__init__(name, age, gender)
        self._id = id
        self._subject = subject
        self._salary = salary

    @property
    def id(self):
        return self._id
    @property
    def subject(self):
        return self._subject
    @property
    def salary(self):
        return self._salary
    
    @id.setter
    def id(self, id):
        if not id.isdigit() or int(id) < 0 or id is None:
            raise ValueError("Invalid ID")
        self._id = id
    @subject.setter
    def subject(self, subject):
        if not isinstance(subject, str) or subject is None:
            raise ValueError("Subject cannot have numbbers or be empty")
        self._subject = subject
    
    @salary.setter
    def salary(self, salary):
        if not salary.isdigit() or int(salary) < 0 or salary is None:
            raise ValueError("Invalid Salary")
        self._salary = salary

    @classmethod
    def get_teacher(cls):
        """
        PSEUDOCODE (Get teacher from user):
          REPEAT
            GET name, age, gender, id, subject, salary (each via required_input so none empty)
            TRY create Teacher, set each attribute (triggers validation)
              IF success THEN RETURN teacher
            CATCH ValueError THEN print error "Please try again", continue loop
          UNTIL valid teacher created
        """
        t = cls(None, None, None, None, None, None)
        # Validate each attribute immediately after user enters it (refill instantly if wrong)
        while True:
            name = required_input("Name: ")
            try:
                t.name = name
                break
            except (ValueError, AttributeError, TypeError) as e:
                print(f"  ✗ Name: {e}. Please re-enter Name.")
        while True:
            age = required_input("Age: ")
            try:
                t.age = age
                break
            except (ValueError, AttributeError, TypeError) as e:
                print(f"  ✗ Age: {e}. Please re-enter Age (positive number).")
        while True:
            gender = required_input("Gender: ")
            try:
                t.gender = gender
                break
            except (ValueError, AttributeError, TypeError) as e:
                print(f"  ✗ Gender: {e}. Please re-enter Gender (Male, Female, or Other).")
        while True:
            id = required_input("ID: ")
            try:
                t.id = id
                break
            except (ValueError, AttributeError, TypeError) as e:
                print(f"  ✗ ID: {e}. Please re-enter ID (positive number).")
        while True:
            subject = required_input("Subject: ")
            try:
                t.subject = subject
                break
            except (ValueError, AttributeError, TypeError) as e:
                print(f"  ✗ Subject: {e}. Please re-enter Subject.")
        while True:
            salary = required_input("Salary: ")
            try:
                t.salary = salary
                break
            except (ValueError, AttributeError, TypeError) as e:
                print(f"  ✗ Salary: {e}. Please re-enter Salary (positive number).")
        return t
    
    def print_teacher(self):
        # PSEUDOCODE: Display teacher name, age, gender, id, subject, salary (one per line)
        print(f"Teacher Name: {self._name} \n Age: {self._age} \n Gender: {self._gender} \n ID: {self._id} \n Subject: {self._subject} \n Salary: ${self._salary}")