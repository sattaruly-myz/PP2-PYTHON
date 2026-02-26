def limited_cycle(lst, k):
    for _ in range(k):
        for item in lst:
            yield item


lst = input().split()
k = int(input())

first = True
for value in limited_cycle(lst, k):
    if not first:
        print(" ", end="")
    print(value, end="")
    first = False