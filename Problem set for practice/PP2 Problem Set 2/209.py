n = int(input())
lis = list(map(int, input().split()))
ma=max(lis)
mi=min(lis)
for i in range(n):
    if lis[i]==ma:
        lis[i]=mi

for j in lis:
    print(j, end=" ")