import re
p = re.compile(r"^\d+$")
s = input()
print("Match" if p.match(s) else "No match")