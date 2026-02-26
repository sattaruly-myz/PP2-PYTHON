import json

def deep_diff(obj1, obj2, path=""):
    diffs = []
    keys = set(obj1.keys()) | set(obj2.keys())
    for key in keys:
        new_path = f"{path}.{key}" if path else key
        val1 = obj1.get(key, "<missing>")
        val2 = obj2.get(key, "<missing>")
        if isinstance(val1, dict) and isinstance(val2, dict):
            diffs.extend(deep_diff(val1, val2, new_path))
        elif val1 != val2:
            if val1 == "<missing>":
                val1_str = "<missing>"
            else:
                val1_str = json.dumps(val1, separators=(',', ':'))
            if val2 == "<missing>":
                val2_str = "<missing>"
            else:
                val2_str = json.dumps(val2, separators=(',', ':'))
            diffs.append(f"{new_path} : {val1_str} -> {val2_str}")
    return diffs

obj1 = json.loads(input())
obj2 = json.loads(input())

differences = deep_diff(obj1, obj2)
if differences:
    for line in sorted(differences):
        print(line)
else:
    print("No differences")