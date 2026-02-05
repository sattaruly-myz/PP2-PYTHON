n=int(input())
lis=list(map(int,input().split()))

seen = set()

for x in lis:
    if x in seen:
        print("NO")
    else:
        print("YES")
        seen.add(x)