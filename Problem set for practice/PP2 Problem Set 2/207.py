n=int(input())
x=list(map(int,input().split()))

f=max(x)

for i in range(n):
    if x[i]==f:
        print(i+1)