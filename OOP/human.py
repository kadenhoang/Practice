def required_input(prompt_text):
    """
    PSEUDOCODE: Prompt until user enters a non-empty value.
      REPEAT
        GET value from user (strip whitespace)
        IF value is not empty THEN RETURN value
        ELSE print "This field is required. Please enter a value."
      UNTIL value is non-empty
    """
    prefix = "  → "
    while True:
        value = input(f"{prefix}{prompt_text}").strip()
        if value:
            return value
        print("  This field is required. Please enter a value.")


class Human:
    def __init__(self, name = None, age = None, gender = None):
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
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        if not name or not name.strip():
            raise ValueError("Invalid Name")
        if name.strip().isdigit():
            raise ValueError("Name cannot be a number")
        allowed = lambda c: c.isalpha() or c.isspace() or c in "-'"
        if not all(allowed(c) for c in name):
            raise ValueError("Name cannot contain special symbols")
        self._name = name
    @age.setter
    def age(self, age):
        if not age.isdigit() or int(age) < 0 or age is None:
            raise ValueError("Invalid Age")
        self._age = age
    @gender.setter
    def gender(self, gender):
        if not gender or not isinstance(gender, str):
            raise ValueError("Invalid Gender")
        g = gender.strip().lower()
        if g not in ("male", "female", "other"):
            raise ValueError("Invalid Gender")
        self._gender = gender.strip().title()

    def get_human(self):
        name = input("Name: ")
        age = input("Age: ")
        gender = input("Gender: ")
        return Human(name,age,gender)
