n = int(input())
lis = list(map(int, input().split()))

max_count = -1
ans = None

for i in range(n):
    count = 1
    for j in range(n-1, i, -1):
        if lis[i] == lis[j]:
            count += 1
    if count > max_count or (count == max_count and lis[i] < ans):
        max_count = count
        ans = lis[i]

print(ans)