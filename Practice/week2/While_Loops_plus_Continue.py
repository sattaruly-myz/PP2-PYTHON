counter = 0
result = []

while counter < 5:
    counter += 1  
    if counter == 3:
        continue
    result.append(counter)

print(result)