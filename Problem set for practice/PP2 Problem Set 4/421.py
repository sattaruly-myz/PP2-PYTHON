import importlib

n = int(input())
for _ in range(n):
    parts = input().split()
    mod_path, attr = parts[0], parts[1]
    try:
        mod = importlib.import_module(mod_path)
    except ModuleNotFoundError:
        print("MODULE_NOT_FOUND")
        continue
    if not hasattr(mod, attr):
        print("ATTRIBUTE_NOT_FOUND")
        continue
    obj = getattr(mod, attr)
    if callable(obj):
        print("CALLABLE")
    else:
        print("VALUE")