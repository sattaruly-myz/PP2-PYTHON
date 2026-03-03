n = int(input())
words = input().split()
print(" ".join(f"{i}:{w}" for i, w in enumerate(words)))