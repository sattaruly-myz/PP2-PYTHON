class Pair:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def add(self, other):
        return Pair(self.a + other.a, self.b + other.b)

a, b, c, d = map(int, input().split())
pair1 = Pair(a, b)
pair2 = Pair(c, d)
result = pair1.add(pair2)
print(f"Result: {result.a} {result.b}")