x=list(map(int,input().split()))
l=list(map(int,input().split()))

for i in range((x[2]-x[1]+1)//2):
    l[x[1]-1+i],l[x[2]-1-i] = l[x[2]-1-i],l[x[1]-1+i]
    

for i in l:
    print(i, end=" ")