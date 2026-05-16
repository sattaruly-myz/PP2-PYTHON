from collections import deque


def flood_fill(surface, pos, new_color):
    x, y = pos
    w, h = surface.get_size()
    target = surface.get_at((x, y))[:3]
    new_color = tuple(new_color[:3])
    if target == new_color:
        return
    queue = deque([(x, y)])
    visited = set() #Чтобы не проверять один и тот же пиксель по кругу миллион раз (иначе программа зависнет)
    visited.add((x, y))
    while queue:
        cx, cy = queue.popleft()
        surface.set_at((cx, cy), new_color)
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                if surface.get_at((nx, ny))[:3] == target:
                    visited.add((nx, ny))
                    queue.append((nx, ny))


def draw_shape(surface, tool, start, end, color, size):
    #surface куда рисовать (холст)
    import math
    x1, y1 = start
    x2, y2 = end
    if tool == 'line':
        pygame_draw_line(surface, color, start, end, size)
    elif tool == 'rect':
        from pygame import draw, Rect
        r = Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        if r.width > 0 and r.height > 0:
            draw.rect(surface, color, r, size)
    elif tool == 'square':
        from pygame import draw, Rect
        s = min(abs(x2 - x1), abs(y2 - y1))
        sx = x1 if x2 >= x1 else x1 - s
        sy = y1 if y2 >= y1 else y1 - s
        if s > 0:
            draw.rect(surface, color, Rect(sx, sy, s, s), size)
    elif tool == 'circle':
        from pygame import draw
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        r = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 / 2)
        if r > 0:
            draw.circle(surface, color, (cx, cy), r, size)
    elif tool == 'rtri':
        from pygame import draw
        pts = [(x1, y2), (x2, y2), (x1, y1)]
        draw.polygon(surface, color, pts, size)
    elif tool == 'etri':
        from pygame import draw
        w = abs(x2 - x1)
        h = int(w * math.sqrt(3) / 2)
        mx = (x1 + x2) // 2
        base_y = y1 + h if y2 >= y1 else y1 - h
        pts = [(x1, base_y), (x2, base_y), (mx, y1)]
        draw.polygon(surface, color, pts, size)
    elif tool == 'rhombus':
        from pygame import draw
        mx = (x1 + x2) // 2
        my = (y1 + y2) // 2
        pts = [(mx, y1), (x2, my), (mx, y2), (x1, my)]
        draw.polygon(surface, color, pts, size)


def pygame_draw_line(surface, color, start, end, size):
    import pygame
    pygame.draw.line(surface, color, start, end, size)