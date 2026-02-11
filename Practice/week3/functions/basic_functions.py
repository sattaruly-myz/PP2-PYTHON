def add_item(item, collection=[]):
    collection.append(item)
    return collection

a = add_item(1)
b = add_item(2)
print(a, b)