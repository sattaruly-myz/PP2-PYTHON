def powers_of_two(n):
    value = 1  # 2^0
    for _ in range(n + 1):
        yield value
        value *= 2


n = int(input())

first = True
for number in powers_of_two(n):
    if not first:
        print(" ", end="")
    print(number, end="")
    first = False