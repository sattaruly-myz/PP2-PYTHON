def divisible_numbers(n):
    for num in range(0, n + 1, 12):  # 12 = lcm(3, 4)
        yield num


n = int(input())

first = True
for number in divisible_numbers(n):
    if not first:
        print(" ", end="")
    print(number, end="")
    first = False