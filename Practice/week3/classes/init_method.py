class Person:
    def __init__(self, name, age=17):
        self.name = name
        self.age = age

p1 = Person("Myrzabek")
p2 = Person("Brawl stars", 67)
print(p1.name, p1.age)
print(p2.name, p2.age)