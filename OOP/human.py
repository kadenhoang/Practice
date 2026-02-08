class Human:
    def __init__(self, name, age, gender):
        self._name = name
        self._age = age
        self._gender = gender

    
    def __str__(self):
        return f"{self._name} is a {self.__gender} aged {self._age} with {self._skind_color} skin."
    
    @property
    def name(self):
        return self._name
    @property
    def age(self):
        return self._age
    @property
    def gender(self):
        return self._gender
    @property
    def skin_color(self):
        return self._skin_color

    @name.setter
    def name(self, name):
        if not name: #check if name is empty or contains only whitespace
            raise ValueError("Invalid Name")
        self._name = name
    @age.setter
    def age(self, age):
        if not age.isdigit() or int(age) < 0 or age is None:
            raise ValueError("Invalid Age")
        self._age = age
    @gender.setter
    def gender(self, gender):
        if not gender in ["Male", "Female", "Other"]:
            raise ValueError("Invalid Gender")
        self._gender = gender

    def get_human(self):
        name = input("Name: ")
        age = input("Age: ")
        gender = input("Gender: ")
        return Human(name,age,gender)
