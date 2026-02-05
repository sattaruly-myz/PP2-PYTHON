n=int(input())
isprime=True
for i in range(2,n):
    if n%i==0:
        isprime=False
        break

if isprime:
    print("Yes")
else:
    print("No")