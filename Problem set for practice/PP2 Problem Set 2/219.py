n = int(input())

epi = dict()

for _ in range(n):
    s, k = input().split()
    k = int(k)
    
    if s in epi:
        epi[s] += k
    else:
        epi[s] = k

for dorama in sorted(epi.keys()):
    print(dorama, epi[dorama])