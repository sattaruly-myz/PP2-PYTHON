# 2. Read and print file contents
with open("sample.txt", "r", encoding="utf-8") as f:
    contents = f.read()

print("File contents:")
print(contents)