n = int(input())

f = True

while n!=1:
    if n%2==1:
        f=False
        break
    else:
        n=n/2

if f:
    print("YES")
else:
    print("NO")