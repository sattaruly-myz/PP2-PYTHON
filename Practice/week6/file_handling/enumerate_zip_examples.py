fruits = ["apple", "banana", "cherry"]
prices = [1.2, 0.5, 2.3]

# 4. enumerate() - index + value
print("enumerate():")
for i, fruit in enumerate(fruits):
    print(f"  {i}: {fruit}")

# zip() - paired iteration
print("\nzip():")
for fruit, price in zip(fruits, prices):
    print(f"  {fruit} costs {price} USD")

# Type checking and conversions
values = ["42", 3.14, True, 100]
print("\nType checking and conversions:")
for v in values:
    print(f"  {v!r:>10} -> type: {type(v).__name__:<8} -> int: {int(float(str(v).replace('True','1')))}")