import json
import re

def resolve_query(data, query):
    current = data
    parts = re.findall(r'\w+|\[\d+\]', query)
    try:
        for part in parts:
            if part.startswith('['):
                index = int(part[1:-1])
                current = current[index]
            else:
                current = current[part]
        return json.dumps(current, separators=(',', ':'))
    except (KeyError, IndexError, TypeError):
        return "NOT_FOUND"

data = json.loads(input())
n = int(input())
queries = [input() for _ in range(n)]

for q in queries:
    print(resolve_query(data, q))