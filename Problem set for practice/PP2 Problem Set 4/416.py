from datetime import datetime, timezone, timedelta
import re

def parse_line(line):
    line = line.strip()
    m = re.match(r'(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) UTC([+-])(\d{2}):(\d{2})', line)
    dt_str = m.group(1) + ' ' + m.group(2)
    sign = 1 if m.group(3) == '+' else -1
    hh, mm = int(m.group(4)), int(m.group(5))
    offset = timezone(timedelta(hours=sign*hh, minutes=sign*mm))
    dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S').replace(tzinfo=offset)
    return dt.astimezone(timezone.utc)

start = parse_line(input())
end = parse_line(input())
print(int((end - start).total_seconds()))