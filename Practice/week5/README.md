# Practice 5 - Python Regular Expressions (RegEx)

## Description
This project demonstrates the use of Python's `re` module to parse a real pharmacy receipt from a text file.

## Files
- `raw.txt` — raw receipt text from EUROPHARMA pharmacy
- `receipt_parser.py` — script that parses the receipt using regex

## What the parser extracts
- Product names
- Prices for each item
- Total amount
- Date and time
- Payment method
- Structured JSON output

## How to run
```bash
python receipt_parser.py
```

## Requirements
- Python 3.x
- No external libraries needed (only built-in `re` and `json`)

## Regex patterns used
- `r"^\d+\.\n(.+)$"` — extract product names
- `r"[\d\s]+,\d{3}\s+x\s+([\d\s]+,\d{2})"` — extract prices
- `r"ИТОГО:\s*\n([\d\s]+,\d{2})"` — extract total amount
- `r"Время:\s+(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})"` — extract date and time
- `r"(Банковская карта|Наличные|Kaspi QR)"` — extract payment method

## Author
Satybaldinov Myrzabek