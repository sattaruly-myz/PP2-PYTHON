class Account:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        if amount > self.balance:
            return False
        self.balance -= amount
        return True

balance, withdraw_amount = map(int, input().split())
account = Account("Owner", balance)

if account.withdraw(withdraw_amount):
    print(account.balance)
else:
    print("Insufficient Funds")