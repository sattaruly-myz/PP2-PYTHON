from functools import reduce

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 1. map() - square each number
squared = list(map(lambda x: x ** 2, numbers))
print("map() - squares:", squared)

# 2. filter() - keep only even numbers
evens = list(filter(lambda x: x % 2 == 0, numbers))
print("filter() - evens:", evens)

# 3. reduce() - sum all numbers
total = reduce(lambda x, y: x + y, numbers)
print("reduce() - sum:", total)

product = reduce(lambda x, y: x * y, numbers)
print("reduce() - product:", product)