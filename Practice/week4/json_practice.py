import json

player = {
    "name": "Myrzabek",
    "university": "KBTU",
    "favorite_game": "Brawl Stars",
    "discipline": "PP2"
}

# превращаем в JSON строку
json_data = json.dumps(player, indent=4)

print("JSON формат:")
print(json_data)

# обратно в словарь
data_back = json.loads(json_data)

print("Имя игрока:", data_back["name"])