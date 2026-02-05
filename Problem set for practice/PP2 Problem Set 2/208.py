n=int(input())

f=1

while f<=n:
    if f*2>n:
        print(f,end=" ")
        break
    else:
        print(f, end=" ")
        f=f*2