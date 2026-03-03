import re
s = input()
m = re.search(r"\S+@\S+\.\S+", s)
print(m.group() if m else "No email")