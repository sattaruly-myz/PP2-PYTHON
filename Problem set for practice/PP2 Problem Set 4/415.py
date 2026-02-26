import math
from datetime import datetime, timezone, timedelta
import re

def parse_line(line):
    line = line.strip()
    m = re.match(r'(\d{4}-\d{2}-\d{2}) UTC([+-])(\d{2}):(\d{2})', line)
    year, month, day = map(int, m.group(1).split('-'))
    sign = 1 if m.group(2) == '+' else -1
    hh, mm = int(m.group(3)), int(m.group(4))
    offset = timezone(timedelta(hours=sign*hh, minutes=sign*mm))
    return datetime(year, month, day, 0, 0, 0, tzinfo=offset), month, day, offset

def is_leap(y):
    return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)

def birthday_dt_in_year(y, bmonth, bday, btz):
    if bmonth == 2 and bday == 29 and not is_leap(y):
        bday = 28
    return datetime(y, bmonth, bday, 0, 0, 0, tzinfo=btz)

birth_dt, bmonth, bday, btz = parse_line(input())
cur_dt, _, _, _ = parse_line(input())
cur_utc = cur_dt.astimezone(timezone.utc)

for year in [cur_dt.year, cur_dt.year + 1]:
    bd_utc = birthday_dt_in_year(year, bmonth, bday, btz).astimezone(timezone.utc)
    diff_sec = (bd_utc - cur_utc).total_seconds()
    if diff_sec >= 0:
        print(math.ceil(diff_sec / 86400))
        break