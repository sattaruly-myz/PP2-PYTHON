epoch = 50
loss = 0.045
dataset = [1, 2, 3]

if 0 < loss < 0.1:
    state = "Converged"
elif 0.1 <= loss < 0.5:
    state = "Learning"
else:
    state = "Unstable"

result = "Ready" if dataset and state == "Converged" else "Not Ready"

print(f"State: {state}")
print(f"Result: {result}")