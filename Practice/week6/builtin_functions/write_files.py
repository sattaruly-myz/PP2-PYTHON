# 1. Create a text file and write sample data
with open("sample.txt", "w", encoding="utf-8") as f:
    f.write("Line 1: Hello, World!\n")
    f.write("Line 2: Python is great\n")
    f.write("Line 3: File handling is easy\n")

print("File created and written successfully.")