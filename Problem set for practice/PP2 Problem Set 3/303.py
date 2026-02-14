word_to_digit = {
    "ZER": "0", "ONE": "1", "TWO": "2", "THR": "3", "FOU": "4",
    "FIV": "5", "SIX": "6", "SEV": "7", "EIG": "8", "NIN": "9"
}

digit_to_word = {v: k for k, v in word_to_digit.items()}

s = input()

i = 0
num1_str = ""
while i < len(s) and s[i:i+3] in word_to_digit:
    num1_str += word_to_digit[s[i:i+3]]
    i += 3

op = s[i]
i += 1

num2_str = ""
while i < len(s):
    num2_str += word_to_digit[s[i:i+3]]
    i += 3

num1 = int(num1_str)
num2 = int(num2_str)

if op == "+":
    result = num1 + num2
elif op == "-":
    result = num1 - num2
else:
    result = num1 * num2

result_str = str(result)
output = ""
for digit in result_str:
    output += digit_to_word[digit]

print(output)