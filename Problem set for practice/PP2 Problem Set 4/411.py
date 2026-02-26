import json

def patch_update(source, patch):
    for key, value in patch.items():
        if value is None:
            if key in source:
                del source[key]
        elif isinstance(value, dict) and isinstance(source.get(key), dict):
            patch_update(source[key], value)
        else:
            source[key] = value
    return source

# читаем вход
source = json.loads(input())
patch = json.loads(input())

result = patch_update(source, patch)

print(json.dumps(result, sort_keys=True, separators=(',', ':')))