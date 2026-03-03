import os

# 1. Create nested directories
os.makedirs("project/src/utils", exist_ok=True)
os.makedirs("project/data/raw", exist_ok=True)
print("Nested directories created.")

# 2. List files and folders
for entry in os.scandir("project"):
    kind = "DIR" if entry.is_dir() else "FILE"
    print(f"  [{kind}] {entry.name}")

# 3. Find files by extension
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".py"):
            print(f"Found .py file: {os.path.join(root, file)}")