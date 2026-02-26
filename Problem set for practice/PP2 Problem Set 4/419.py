import math, sys

data = sys.stdin.read().split()
r = float(data[0])
ax, ay = float(data[1]), float(data[2])
bx, by = float(data[3]), float(data[4])

da = math.sqrt(ax*ax + ay*ay)
db = math.sqrt(bx*bx + by*by)

dx = bx - ax
dy = by - ay
direct = math.sqrt(dx*dx + dy*dy)

a_dot_d = ax*dx + ay*dy
t_min = -a_dot_d / (direct*direct) if direct > 0 else 0
t_min = max(0.0, min(1.0, t_min))
cx = ax + t_min*dx
cy = ay + t_min*dy
min_dist = math.sqrt(cx*cx + cy*cy)

if min_dist >= r - 1e-9:
    print(f"{direct:.10f}")
else:
    angle_a = math.atan2(ay, ax)
    angle_b = math.atan2(by, bx)
    
    tan_a = math.sqrt(max(0, da*da - r*r))
    tan_b = math.sqrt(max(0, db*db - r*r))
    
    alpha_a = math.acos(max(-1, min(1, r/da))) if da > r else 0
    alpha_b = math.acos(max(-1, min(1, r/db))) if db > r else 0
    
    
    best = float('inf')
    for sa in [1, -1]:
        ta_angle = angle_a + sa * alpha_a
        for sb in [1, -1]:
            tb_angle = angle_b + sb * alpha_b
            arc = abs(ta_angle - tb_angle)
            arc = min(arc, 2*math.pi - arc)
            total = tan_a + r * arc + tan_b
            best = min(best, total)
    
    print(f"{best:.10f}")