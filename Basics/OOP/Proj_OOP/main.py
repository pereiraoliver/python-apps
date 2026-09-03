class User:
    def __init__(self, name, birthyear):
        self.name = name
        self.birthyear = birthyear

    def get_name(self):
        return self.name.upper()

    def age(self, current_year=2023):
        return current_year - self.birthyear


user = User("John", 1999)
print(user.age())
print(user.get_name())
