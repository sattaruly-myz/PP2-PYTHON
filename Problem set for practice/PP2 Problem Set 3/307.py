class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def show(self):
        print(f"({self.x}, {self.y})")
    
    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
    
    def dist(self, other_point):
        return ((self.x - other_point.x) ** 2 + (self.y - other_point.y) ** 2) ** 0.5

x1, y1 = map(int, input().split())
point1 = Point(x1, y1)
point1.show()

x2, y2 = map(int, input().split())
point1.move(x2, y2)
point1.show()

x3, y3 = map(int, input().split())
point2 = Point(x3, y3)
distance = point1.dist(point2)
print(f"{distance:.2f}")