def squares(n):
    for number in range(1, n + 1):
        yield number * number


n = int(input())

for square in squares(n):
    print(square)