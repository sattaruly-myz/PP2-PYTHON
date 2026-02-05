n=int(input())
lis=list()

for i in range(n):
    lis.append(input())

count = dict()

for number in lis:
    if number in count:
        count[number] += 1
    else:
        count[number] = 1

ans = 0
for number in count:
    if count[number] == 3:
        ans += 1

print(ans)