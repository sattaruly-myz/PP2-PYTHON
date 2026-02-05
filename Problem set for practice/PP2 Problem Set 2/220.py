n = int(input())
document = {}

for i in range(n):
    line = input()
    parts = line.split()
    command = parts[0]
    
    if command == "set":
        key = parts[1]
        value = parts[2]
        document[key] = value
    elif command == "get":
        key = parts[1]
        if key in document:
            print(document[key])
        else:
            print("KE: no key " + key + " found in the document")