import re
s = input()
print("Yes" if re.match(r"^[A-Za-z].*\d$", s) else "No")