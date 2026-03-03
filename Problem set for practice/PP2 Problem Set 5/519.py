import re
p = re.compile(r"\b\w+\b")
s = input()
print(len(p.findall(s)))