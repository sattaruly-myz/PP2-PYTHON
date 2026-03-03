import re
s = input()
p = input()
print(len(re.findall(re.escape(p), s)))