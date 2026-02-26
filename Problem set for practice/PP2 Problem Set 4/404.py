def squares(a, b):
    for number in range(a, b + 1):
        yield number * number


a, b = map(int, input().split())

for value in squares(a, b):
    print(value)