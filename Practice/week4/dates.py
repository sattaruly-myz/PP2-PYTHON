from datetime import datetime

# дедлайн
deadline = datetime(2026, 3, 5)
today = datetime.now()

difference = deadline - today

print("Осталось дней:", difference.days)