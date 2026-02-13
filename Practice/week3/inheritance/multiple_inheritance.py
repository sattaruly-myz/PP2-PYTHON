class Asset:
    def __init__(self):
        print("Asset init")

class Stock(Asset):
    def __init__(self):
        super().__init__()
        print("Stock init")

class Bond(Asset):
    def __init__(self):
        super().__init__()
        print("Bond init")

class Portfolio(Stock, Bond):
    def __init__(self):
        super().__init__()
        print("Portfolio init")

p = Portfolio()