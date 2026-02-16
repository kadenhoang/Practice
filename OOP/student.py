import string
from human import Human, required_input


class Student(Human):
    
    def __init__(self, name = None, age = None, gender = None, id = None, major = None):
        super().__init__(name, age, gender)
        self._id = id
        self._major = major

    @property
    def id(self):
        return self._id
    @property
    def major(self):
        return self._major
    
    @id.setter
    def id(self, id):
        if not id.isdigit() or int(id) < 0 or id is None:
            raise ValueError("Invalid ID")
        self._id = id

    @major.setter
    def major(self, major):
        if not isinstance(major, str) or major is None:
            raise ValueError("Major cannot have numbbers or be empty")
        self._major = major

    @classmethod
    def get_student(cls):
        """
        PSEUDOCODE (Get student from user):
          REPEAT
            GET name, age, gender, id, major (each via required_input so none empty)
            TRY create Student, set each attribute (triggers validation)
              IF success THEN RETURN student
            CATCH ValueError THEN print error "Please try again", continue loop
          UNTIL valid student created
        """
        s = cls(None, None, None, None, None)
        # Validate each attribute immediately after user enters it (refill instantly if wrong)
        while True:
            name = required_input("Name: ")
            try:
                s.name = name
                break
            except (ValueError, AttributeError, TypeError) as e:
                print(f"  ✗ Name: {e}. Please re-enter Name.")
        while True:
            age = required_input("Age: ")
            try:
                s.age = age
                break
            except (ValueError, AttributeError, TypeError) as e:
                print(f"  ✗ Age: {e}. Please re-enter Age (positive number).")
        while True:
            gender = required_input("Gender: ")
            try:
                s.gender = gender
                break
            except (ValueError, AttributeError, TypeError) as e:
                print(f"  ✗ Gender: {e}. Please re-enter Gender (Male, Female, or Other).")
        while True:
            id = required_input("ID: ")
            try:
                s.id = id
                break
            except (ValueError, AttributeError, TypeError) as e:
                print(f"  ✗ ID: {e}. Please re-enter ID (positive number).")
        while True:
            major = required_input("Major: ")
            try:
                s.major = major
                break
            except (ValueError, AttributeError, TypeError) as e:
                print(f"  ✗ Major: {e}. Please re-enter Major.")
        return s
    
    def print_student(self):
        # PSEUDOCODE: Display student name, age, gender, id, major (one per line)
        print(f"Student Name: {self._name} \n Age: {self._age} \n Gender: {self._gender} \n ID: {self._id} \n Major: {self._major}")