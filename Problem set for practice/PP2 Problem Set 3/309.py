import math

class Circle:
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return math.pi * self.radius * self.radius

radius = int(input())
circle = Circle(radius)
print(f"{circle.area():.2f}")