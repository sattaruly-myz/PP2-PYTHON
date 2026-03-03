n = int(input())
print("Yes" if all(x >= 0 for x in map(int, input().split())) else "No")