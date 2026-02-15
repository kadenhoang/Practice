import string
from human import Human


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
        name = input("Name: ")
        age = input("Age: ")
        gender = input("Gender: ")
        id = input("ID: ")
        major = input("Major: ")
        return cls(name, age, gender, id, major)
    
    def print_student(self):
        print(f"Student Name: {self._name} \n Age: {self._age} \n Gender: {self._gender} \n ID: {self._id} \n Major: {self._major}")