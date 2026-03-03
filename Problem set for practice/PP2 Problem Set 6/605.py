s = input()
print("Yes" if any(c.lower() in "aeiou" for c in s) else "No")