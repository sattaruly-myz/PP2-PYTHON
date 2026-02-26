def kbtu_disciplines():
    disciplines = ["Calculus", "Physics", "Programming", "Brawl_Stars_Theory"]
    for discipline in disciplines:
        yield discipline  # генератор возвращает по одному значению

# создаем генератор
gen = kbtu_disciplines()

print(next(gen))  # Calculus
print(next(gen))  # Physics

# Многие забывают, что генератор "заканчивается"
for item in gen:
    print(item)

# Если снова сделать:
for item in gen:
    print(item)   # НИЧЕГО не выведется (генератор уже пуст)