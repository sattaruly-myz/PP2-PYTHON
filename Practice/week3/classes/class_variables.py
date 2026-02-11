class Dog:
    species = "Canine"

d1 = Dog()
d2 = Dog()
d1.species = "Wolf"
print(d1.species)
print(d2.species)
print(Dog.species)