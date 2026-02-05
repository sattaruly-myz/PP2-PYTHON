accuracy = float(input())
grade = ""

if accuracy >= 0.90:
    grade = "A"
elif accuracy >= 0.80:
    grade = "B"
elif accuracy >= 0.70:
    grade = "C"
else:
    grade = "F"

print(f"Model Grade: {grade}")