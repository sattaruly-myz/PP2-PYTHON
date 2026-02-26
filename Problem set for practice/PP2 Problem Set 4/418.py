import sys
data = sys.stdin.read().split()
ax, ay = float(data[0]), float(data[1])
bx, by = float(data[2]), float(data[3])
t = ay / (ay + by)
rx = ax + t * (bx - ax)
print(f"{rx:.10f} 0.0000000000")