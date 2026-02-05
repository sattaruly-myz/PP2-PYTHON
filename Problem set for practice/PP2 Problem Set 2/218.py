n=int(input())
lis=list()

for i in range(n):
    lis.append(input())

first_index = dict()

for i in range(n):
    s = lis[i]
    if s not in first_index:
        first_index[s] = i + 1

for s in sorted(first_index.keys()):
    print(s, first_index[s])