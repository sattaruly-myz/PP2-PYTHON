packets = [10, 25, 40, 12, 55]
limit = 100

for p in packets:
    if p > limit:
        print("Danger found!")
        break
else:
    print("All packets follow protocol")