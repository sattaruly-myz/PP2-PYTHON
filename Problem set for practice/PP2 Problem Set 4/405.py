def countdown(n):
    for number in range(n, -1, -1):
        yield number


n = int(input())

for value in countdown(n):
    print(value)