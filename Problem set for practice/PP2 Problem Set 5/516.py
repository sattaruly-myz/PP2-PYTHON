import re
s = input()
m = re.search(r"Name: (.+), Age: (.+)", s)
print(m.group(1), m.group(2))