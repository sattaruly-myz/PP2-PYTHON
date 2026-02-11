def combine(*args, **kwargs):
    result = sum(args)
    for key in kwargs:
        result += kwargs[key]
    return result

print(combine(1, 2, 3, a=4, b=5))