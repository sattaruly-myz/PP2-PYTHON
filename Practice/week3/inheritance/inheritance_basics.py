class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def work(self):
        print(f"{self.name} works")

class Manager(Employee):
    pass

class Developer(Employee):
    pass

m = Manager("Myrzabek", 50000)
d = Developer("CR7", 60000)