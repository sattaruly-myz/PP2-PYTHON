class Counter:
    count = 0 

    def __init__(self):
        Counter.count += 1  

    def show_count(self):
        return Counter.count

c1 = Counter()
c2 = Counter()
c3 = Counter()

print(c1.show_count())
print(c2.show_count())
print(Counter.count)