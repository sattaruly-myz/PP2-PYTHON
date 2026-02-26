n_cmds = int(input())
g = 0
n = 0
for _ in range(n_cmds):
    parts = input().split()
    scope, val = parts[0], int(parts[1])
    if scope == 'global':
        g += val
    elif scope == 'nonlocal':
        n += val
print(g, n)