import shutil
import os

# 3. Append new lines and verify content
with open("sample.txt", "a", encoding="utf-8") as f:
    f.write("Line 4: Appended line\n")

with open("sample.txt", "r", encoding="utf-8") as f:
    print("After append:")
    print(f.read())

# 4. Copy and back up files using shutil
shutil.copy("sample.txt", "sample_backup.txt")
print("Backup created: sample_backup.txt")

# 5. Delete files safely
if os.path.exists("sample_backup.txt"):
    os.remove("sample_backup.txt")
    print("Backup deleted safely.")