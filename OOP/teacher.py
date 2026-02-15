from human import Human
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
        name = input("Name: ")
        age = input("Age: ")
        gender = input("Gender: ")
        id = input("ID: ")
        subject = input("Subject: ")
        salary = input("Salary: ")
        return cls(name, age, gender, id, subject, salary)
    
    def print_teacher(self):
        print(f"Teacher Name: {self._name} \n Age: {self._age} \n Gender: {self._gender} \n ID: {self._id} \n Subject: {self._subject} \n Salary: ${self._salary}")