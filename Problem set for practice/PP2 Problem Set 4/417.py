import math, sys
data = sys.stdin.read().split()
r = float(data[0])
ax, ay = float(data[1]), float(data[2])
bx, by = float(data[3]), float(data[4])

dx, dy = bx - ax, by - ay
fx, fy = ax, ay  # origin is (0,0)

a = dx*dx + dy*dy
b = 2*(fx*dx + fy*dy)
c = fx*fx + fy*fy - r*r

if a == 0:
    print(f"{0:.10f}")
else:
    disc = b*b - 4*a*c
    if disc <= 0:
        print(f"{0:.10f}")
    else:
        sq = math.sqrt(disc)
        t1 = max((-b - sq) / (2*a), 0.0)
        t2 = min((-b + sq) / (2*a), 1.0)
        if t2 <= t1:
            print(f"{0:.10f}")
        else:
            print(f"{(t2-t1)*math.sqrt(a):.10f}")