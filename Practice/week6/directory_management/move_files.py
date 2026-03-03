import shutil
import os

# 4. Move/copy files between directories
os.makedirs("project/data/raw", exist_ok=True)

with open("temp.txt", "w") as f:
    f.write("Temporary file content")

shutil.copy("temp.txt", "project/data/raw/temp_copy.txt")
print("File copied to project/data/raw/")

shutil.move("temp.txt", "project/data/raw/temp_moved.txt")
print("File moved to project/data/raw/")