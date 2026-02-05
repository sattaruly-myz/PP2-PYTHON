data = list(map(int, input().split()))

for item in data[:]: 
    if item > sum(data) / len(data):
        data.remove(item)

print(data)