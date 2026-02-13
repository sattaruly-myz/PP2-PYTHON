class Base:
    def __init__(self):
        print("Base init")

class Child(Base):
    def __init__(self):
        super().__init__()
        print("Child init")

c = Child()