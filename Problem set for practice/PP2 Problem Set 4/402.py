def even_numbers(n):
    for num in range(0, n + 1, 2):
        yield num


n = int(input())

first = True
for number in even_numbers(n):
    if not first:
        print(",", end="")
    print(number, end="")
    first = False