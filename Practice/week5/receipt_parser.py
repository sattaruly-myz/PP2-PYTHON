import re
import json

with open(r"c:\Users\satyb\OneDrive\Desktop\second sem KBTU\PP2 PYTHON\Practice\week5\raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Товары: номер -> название -> количество x цена -> итог
blocks = re.findall(
    r"^\d+\.\n(.+?)\n[\d\s]+,\d{3}\s+x\s+([\d\s]+,\d{2})",
    text, re.MULTILINE
)

items = []
for name, price in blocks:
    price_clean = float(price.replace(" ", "").replace(",", "."))
    items.append({"название": name.strip(), "цена": price_clean})

# 2. Итого
total_match = re.search(r"ИТОГО:\s*\n([\d\s]+,\d{2})", text)
total = float(total_match.group(1).replace(" ", "").replace(",", ".")) if total_match else 0.0

# 3. Дата и время
dt_match = re.search(r"Время:\s+(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})", text)
date = dt_match.group(1) if dt_match else "Не найдено"
time_val = dt_match.group(2) if dt_match else "Не найдено"

# 4. Способ оплаты
payment_match = re.search(r"(Банковская карта|Наличные|Kaspi QR)", text)
payment = payment_match.group(1) if payment_match else "Не найдено"

# 5. Вывод
receipt = {
    "магазин": "EUROPHARMA",
    "дата": date,
    "время": time_val,
    "способ_оплаты": payment,
    "товары": items,
    "итого": total
}

print("=" * 45)
print("       РЕЗУЛЬТАТ ПАРСИНГА ЧЕКА")
print("=" * 45)
print(f"Магазин:   EUROPHARMA")
print(f"Дата:      {date}")
print(f"Время:     {time_val}")
print(f"Оплата:    {payment}")
print(f"Итого:     {total:.2f} тг")
print()
print(f"Товары ({len(items)} позиций):")
for i, item in enumerate(items, 1):
    print(f"  {i:>2}. {item['название'][:45]:<45} {item['цена']:>9.2f} тг")
print()
print("JSON:")
print(json.dumps(receipt, ensure_ascii=False, indent=2))