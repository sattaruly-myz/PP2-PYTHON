import random
import math

kbtu_students = ["Aruzhan", "Dias", "Miras"]

for student in kbtu_students:
    score = random.randint(0, 100)  # 100 тоже может выпасть!
    rounded = math.ceil(score / 10) * 10
    
    print(f"{student} получил {score}, округлили до {rounded}")