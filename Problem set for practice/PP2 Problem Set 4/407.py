class Reverse:
    def __init__(self, text):
        self.text = text
        self.index = len(text) - 1  # начинаем с последнего символа

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < 0:
            raise StopIteration
        char = self.text[self.index]
        self.index -= 1
        return char


s = input()

for ch in Reverse(s):
    print(ch, end="")