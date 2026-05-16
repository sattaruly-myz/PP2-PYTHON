import pygame
import sys
from datetime import datetime
from tools import flood_fill, draw_shape

pygame.init()

WIDTH, HEIGHT = 1150, 680
SIDEBAR = 130
CANVAS_W = WIDTH - SIDEBAR
CANVAS_H = HEIGHT

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
DARK = (60, 60, 60)
PANEL = (220, 220, 225)
ACTIVE = (70, 130, 200)

PALETTE = [
    (0, 0, 0),       (255, 255, 255), (127, 127, 127), (195, 195, 195),
    (255, 0, 0),     (180, 0, 0),     (255, 140, 0),   (180, 90, 0),
    (255, 255, 0),   (160, 160, 0),   (0, 200, 0),     (0, 120, 0),
    (0, 220, 220),   (0, 120, 120),   (0, 80, 255),    (0, 0, 160),
    (220, 0, 220),   (130, 0, 130),   (255, 180, 200), (139, 90, 43),
]

TOOLS = [
    'pencil', 'line',
    'rect',   'square',
    'circle', 'rtri',
    'etri',   'rhombus',
    'eraser', 'fill',
    'text',   'picker',
]

LABELS = {
    'pencil': 'Pencil',  'line':   'Line',
    'rect':   'Rect',    'square': 'Square',
    'circle': 'Circle',  'rtri':   'R.Tri',
    'etri':   'E.Tri',   'rhombus':'Rhombus',
    'eraser': 'Eraser',  'fill':   'Fill',
    'text':   'Text',    'picker': 'Picker',
}

SIZES = [2, 5, 10]
SHAPE_TOOLS = ('line', 'rect', 'square', 'circle', 'rtri', 'etri', 'rhombus')

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

canvas = pygame.Surface((CANVAS_W, CANVAS_H))
canvas.fill(WHITE)

fn = pygame.font.SysFont('Arial', 11)
ft = pygame.font.SysFont('Arial', 24)

tool = 'pencil'
color = BLACK
size_idx = 0
size = SIZES[0]

drawing = False
start_pos = None
last_pos = None

text_on = False
text_pos = None
text_buf = ''


def sid_tool(i): #2 колонки
    r, c = divmod(i, 2)
    return pygame.Rect(4 + c * 62, 4 + r * 28, 60, 26)


def sid_size(i): #Расставляет кнопки выбора толщины кисти в одну горизонтальную линию
    return pygame.Rect(4 + i * 40, 4 + 6 * 28 + 6, 38, 24)


def sid_color(i):
    base_y = 4 + 6 * 28 + 6 + 28 + 36
    r, c = divmod(i, 4)
    return pygame.Rect(4 + c * 30, base_y + r * 24, 28, 22)


def draw_sidebar():
    pygame.draw.rect(screen, PANEL, (0, 0, SIDEBAR, HEIGHT))
    pygame.draw.line(screen, GRAY, (SIDEBAR, 0), (SIDEBAR, HEIGHT), 2)

    for i, t in enumerate(TOOLS):
        rect = sid_tool(i)
        bg = ACTIVE if t == tool else GRAY
        pygame.draw.rect(screen, bg, rect, border_radius=3)
        pygame.draw.rect(screen, DARK, rect, 1, border_radius=3)
        lbl = fn.render(LABELS[t], True, WHITE if t == tool else DARK)
        screen.blit(lbl, (rect.x + 2, rect.y + 7))

    size_y = 4 + 6 * 28 + 2 # размер кисты
    screen.blit(fn.render('Size:', True, DARK), (4, size_y))
    for i, s in enumerate(SIZES):
        rect = sid_size(i)
        bg = ACTIVE if i == size_idx else GRAY
        pygame.draw.rect(screen, bg, rect, border_radius=3)
        pygame.draw.rect(screen, DARK, rect, 1, border_radius=3)
        lbl = fn.render(f'{i+1}:{s}px', True, WHITE if i == size_idx else DARK)
        screen.blit(lbl, (rect.x + 3, rect.y + 6))

    base_y = 4 + 6 * 28 + 6 + 28 #текущий цвет
    screen.blit(fn.render('Color:', True, DARK), (4, base_y + 4))
    pygame.draw.rect(screen, color, (68, base_y, 52, 28))
    pygame.draw.rect(screen, DARK, (68, base_y, 52, 28), 1)

    for i, c in enumerate(PALETTE):
        rect = sid_color(i)
        pygame.draw.rect(screen, c, rect)
        pygame.draw.rect(screen, DARK, rect, 1)


def cpos(mx, my): # чтобы не рисовал в понел инструментов
    return mx - SIDEBAR, my


clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            mods = pygame.key.get_mods()

            if event.key == pygame.K_1:
                size_idx = 0; size = SIZES[0]
            elif event.key == pygame.K_2:
                size_idx = 1; size = SIZES[1]
            elif event.key == pygame.K_3:
                size_idx = 2; size = SIZES[2]

            if event.key == pygame.K_s and (mods & pygame.KMOD_CTRL):
                fname = 'canvas_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.png'
                pygame.image.save(canvas, fname)

            if text_on:
                if event.key == pygame.K_RETURN:
                    surf = ft.render(text_buf, True, color)
                    canvas.blit(surf, text_pos)
                    text_on = False; text_buf = ''; text_pos = None
                elif event.key == pygame.K_ESCAPE:
                    text_on = False; text_buf = ''; text_pos = None
                elif event.key == pygame.K_BACKSPACE:
                    text_buf = text_buf[:-1]
                elif event.unicode and event.unicode.isprintable():
                    text_buf += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            if mx < SIDEBAR:
                for i, t in enumerate(TOOLS):
                    if sid_tool(i).collidepoint(mx, my):
                        tool = t
                        text_on = False; text_buf = ''
                for i in range(3):
                    if sid_size(i).collidepoint(mx, my):
                        size_idx = i; size = SIZES[i]
                for i, c in enumerate(PALETTE):
                    if sid_color(i).collidepoint(mx, my):
                        color = c
            else:
                cx, cy = cpos(mx, my)
                cx = max(0, min(CANVAS_W - 1, cx))
                cy = max(0, min(CANVAS_H - 1, cy))

                if tool == 'picker':
                    color = canvas.get_at((cx, cy))[:3]
                elif tool == 'fill':
                    flood_fill(canvas, (cx, cy), color)
                elif tool == 'text':
                    text_on = True; text_pos = (cx, cy); text_buf = ''
                else:
                    drawing = True
                    start_pos = (cx, cy)
                    last_pos = (cx, cy)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if drawing:
                mx, my = event.pos
                cx = max(0, min(CANVAS_W - 1, mx - SIDEBAR))
                cy = max(0, min(CANVAS_H - 1, my))
                if tool in SHAPE_TOOLS:
                    draw_shape(canvas, tool, start_pos, (cx, cy), color, size)
                drawing = False; start_pos = None; last_pos = None

        if event.type == pygame.MOUSEMOTION:
            if drawing:
                mx, my = event.pos
                cx = max(0, min(CANVAS_W - 1, mx - SIDEBAR))
                cy = max(0, min(CANVAS_H - 1, my))
                if tool == 'pencil':
                    pygame.draw.line(canvas, color, last_pos, (cx, cy), size)
                    last_pos = (cx, cy)
                elif tool == 'eraser':
                    pygame.draw.line(canvas, WHITE, last_pos, (cx, cy), size * 3)
                    last_pos = (cx, cy)
                else:
                    last_pos = (cx, cy)

    screen.fill(PANEL)

    if drawing and start_pos and tool in SHAPE_TOOLS:
        preview = canvas.copy()
        draw_shape(preview, tool, start_pos, last_pos, color, size)
        screen.blit(preview, (SIDEBAR, 0))
    else:
        screen.blit(canvas, (SIDEBAR, 0))

    if text_on and text_pos:
        ts = ft.render(text_buf + '|', True, color)
        screen.blit(ts, (text_pos[0] + SIDEBAR, text_pos[1]))

    draw_sidebar()
    pygame.display.flip()
    clock.tick(60)