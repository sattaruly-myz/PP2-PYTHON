import pygame
from pygame.locals import *
import sys
import math

pygame.init()

#  НАСТРОЙКИ ОКНА 
SCREEN_WIDTH  = 1200
SCREEN_HEIGHT = 700
PANEL_HEIGHT  = 120    # высота нижней панели инструментов (увеличена для 2 рядов)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Paint Application")

#  ЦВЕТА 
WHITE  = (255, 255, 255)
BLACK  = (  0,   0,   0)
RED    = (255,   0,   0)
GREEN  = (  0, 255,   0)
BLUE   = (  0,   0, 255)
YELLOW = (255, 255,   0)
ORANGE = (255, 165,   0)
PURPLE = (128,   0, 128)
PINK   = (255, 192, 203)
GRAY   = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

# Область рисования — всё, кроме нижней панели
CANVAS_Y     = SCREEN_HEIGHT - PANEL_HEIGHT
CANVAS_RECT  = pygame.Rect(0, 0, SCREEN_WIDTH, CANVAS_Y)

#  ИНСТРУМЕНТЫ 
TOOL_BRUSH      = 'brush'
TOOL_RECTANGLE  = 'rectangle'
TOOL_SQUARE     = 'square'           # новый: квадрат (равные стороны)
TOOL_CIRCLE     = 'circle'
TOOL_ERASER     = 'eraser'
TOOL_RIGHT_TRI  = 'right_triangle'  # новый: прямоугольный треугольник
TOOL_EQ_TRI     = 'eq_triangle'     # новый: равносторонний треугольник
TOOL_RHOMBUS    = 'rhombus'         # новый: ромб

# Текущее состояние
current_tool      = TOOL_BRUSH
current_color     = BLACK
brush_size        = 5
drawing_shape     = False
shape_start_pos   = None

#  ПАЛИТРА ЦВЕТОВ 
# Расположена в левой части нижней панели
PALETTE_Y = SCREEN_HEIGHT - PANEL_HEIGHT + 10

color_palette = [
    (BLACK,  pygame.Rect(10,  PALETTE_Y,      50, 50)),
    (RED,    pygame.Rect(68,  PALETTE_Y,      50, 50)),
    (GREEN,  pygame.Rect(126, PALETTE_Y,      50, 50)),
    (BLUE,   pygame.Rect(184, PALETTE_Y,      50, 50)),
    (YELLOW, pygame.Rect(242, PALETTE_Y,      50, 50)),
    (ORANGE, pygame.Rect(300, PALETTE_Y,      50, 50)),
    (PURPLE, pygame.Rect(358, PALETTE_Y,      50, 50)),
    (PINK,   pygame.Rect(416, PALETTE_Y,      50, 50)),
]

#  КНОПКИ ИНСТРУМЕНТОВ (2 ряда по 4) 
# Первый ряд: базовые инструменты
# Второй ряд: новые фигуры
BTN_X0    = 490    # начало первой кнопки по X
BTN_W     = 82     # ширина кнопки
BTN_GAP   = 5      # зазор между кнопками
BTN_H     = 48     # высота кнопки
ROW1_Y    = SCREEN_HEIGHT - PANEL_HEIGHT + 8
ROW2_Y    = ROW1_Y + BTN_H + 8

def _btn(col, row):
    """Возвращает Rect для кнопки по индексу колонки и ряда (0-based)."""
    x = BTN_X0 + col * (BTN_W + BTN_GAP)
    y = ROW1_Y if row == 0 else ROW2_Y
    return pygame.Rect(x, y, BTN_W, BTN_H)

# Словарь: инструмент → (Rect, метка)
tool_buttons = {
    TOOL_BRUSH:     (_btn(0, 0), "Brush"),
    TOOL_RECTANGLE: (_btn(1, 0), "Rect"),
    TOOL_CIRCLE:    (_btn(2, 0), "Circle"),
    TOOL_ERASER:    (_btn(3, 0), "Eraser"),
    TOOL_SQUARE:    (_btn(0, 1), "Square"),
    TOOL_RIGHT_TRI: (_btn(1, 1), "R.Tri"),
    TOOL_EQ_TRI:    (_btn(2, 1), "E.Tri"),
    TOOL_RHOMBUS:   (_btn(3, 1), "Rhombus"),
}

#  КНОПКА «ОЧИСТИТЬ» 
clear_button = pygame.Rect(SCREEN_WIDTH - 110,
                           SCREEN_HEIGHT - PANEL_HEIGHT + (PANEL_HEIGHT - 60) // 2,
                           100, 60)

#  ХОЛСТ 
canvas = pygame.Surface((SCREEN_WIDTH, CANVAS_Y))
canvas.fill(WHITE)

font       = pygame.font.Font(None, 22)
font_small = pygame.font.Font(None, 19)
last_pos   = None


#  ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ: РИСОВАНИЕ ЛИНИИ 

def draw_line(surface, color, start, end, width):
    """
    Рисует гладкую линию между двумя точками, заполняя промежуточные
    пиксели маленькими кругами. Используется для кисти и ластика.
    """
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))

    if distance > 0:
        for i in range(int(distance)):
            x = int(start[0] + float(i) / distance * dx)
            y = int(start[1] + float(i) / distance * dy)
            pygame.draw.circle(surface, color, (x, y), width)


#  ВЫЧИСЛЕНИЕ ВЕРШИН ФИГУР 

def square_rect(p1, p2):
    """
    Возвращает pygame.Rect для квадрата.
    Сторона квадрата = минимум из |dx| и |dy|, чтобы сохранить пропорции 1:1.
    """
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    side = min(abs(dx), abs(dy))                # квадрат — равные стороны
    # Знак определяет, в какую сторону «тянем» квадрат
    sx = side if dx >= 0 else -side
    sy = side if dy >= 0 else -side
    x = min(p1[0], p1[0] + sx)
    y = min(p1[1], p1[1] + sy)
    return pygame.Rect(x, y, side, side)


def right_triangle_points(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    return [
        (x1, y1),
        (x2, y1),
        (x1, y2),
    ]


def equilateral_triangle_points(p1, p2):
    """
    Вычисляет вершины правильного (равностороннего) треугольника.
    Основание: от p1 до (p2.x, p1.y).
    Апекс расположен перпендикулярно над серединой основания
    на высоте h = sqrt(3)/2 * основание.
    Треугольник строится «вниз» (p2.y > p1.y) или «вверх».
    """
    x1, y1 = p1
    x2, y2 = p2
    base = x2 - x1                             # длина основания со знаком
    # Высота равностороннего треугольника
    h = math.sqrt(3) / 2 * abs(base)
    # Направление апекса определяется тем, куда тянем мышь по Y
    direction = 1 if y2 > y1 else -1
    mid_x = (x1 + x2) / 2
    apex  = (int(mid_x), int(y1 + direction * h))
    return [(x1, y1), (x2, y1), apex]


def rhombus_points(p1, p2):
    """
    Вычисляет вершины ромба.
    Центр ромба — точка p1.
    Полудиагонали: |dx| по горизонтали, |dy| по вертикали.
    Вершины: верхняя, правая, нижняя, левая.
    """
    cx, cy = p1
    dx = abs(p2[0] - cx)
    dy = abs(p2[1] - cy)
    return [
        (cx,      cy - dy),   # верхняя
        (cx + dx, cy),        # правая
        (cx,      cy + dy),   # нижняя
        (cx - dx, cy),        # левая
    ]


#  ОТРИСОВКА ФИГУРЫ НА ПОВЕРХНОСТИ 

def draw_shape(surface, tool, p1, p2, color, width=0):
    """
    Рисует выбранную фигуру на указанной поверхности (canvas или screen).
    width=0 означает заливку; width>0 — только контур.
    Поддерживает все восемь инструментов-фигур.
    """
    if tool == TOOL_RECTANGLE:
        x1, y1 = p1
        x2, y2 = p2
        r = pygame.Rect(min(x1,x2), min(y1,y2), abs(x2-x1), abs(y2-y1))
        pygame.draw.rect(surface, color, r, width)

    elif tool == TOOL_SQUARE:
        r = square_rect(p1, p2)
        pygame.draw.rect(surface, color, r, width)

    elif tool == TOOL_CIRCLE:
        x1, y1 = p1
        x2, y2 = p2
        radius = int(math.hypot(x2 - x1, y2 - y1))
        if radius > 0:
            pygame.draw.circle(surface, color, (x1, y1), radius, width or brush_size)

    elif tool == TOOL_RIGHT_TRI:
        pts = right_triangle_points(p1, p2)
        pygame.draw.polygon(surface, color, pts, width)

    elif tool == TOOL_EQ_TRI:
        pts = equilateral_triangle_points(p1, p2)
        pygame.draw.polygon(surface, color, pts, width)

    elif tool == TOOL_RHOMBUS:
        pts = rhombus_points(p1, p2)
        pygame.draw.polygon(surface, color, pts, width)


#  ИНТЕРФЕЙС 

def draw_interface():
    """
    Рисует нижнюю панель:
    - фон панели и разделительная линия
    - палитру цветов (с рамкой у текущего цвета)
    - кнопки инструментов (два ряда)
    - кнопку «Clear»
    """
    # Фон панели
    pygame.draw.rect(screen, (45, 45, 55),
                     (0, CANVAS_Y, SCREEN_WIDTH, PANEL_HEIGHT))
    pygame.draw.line(screen, GRAY, (0, CANVAS_Y), (SCREEN_WIDTH, CANVAS_Y), 1)

    #  Палитра цветов 
    for color, rect in color_palette:
        pygame.draw.rect(screen, color, rect, border_radius=6)
        # Белая рамка у выбранного цвета
        if color == current_color:
            pygame.draw.rect(screen, WHITE, rect, 3, border_radius=6)
        else:
            pygame.draw.rect(screen, (80, 80, 90), rect, 1, border_radius=6)

    #  Кнопки инструментов 
    for tool, (rect, label) in tool_buttons.items():
        # Активный инструмент выделяется ярким фоном
        if tool == current_tool:
            bg = (  0, 180, 220)   # голубой — активный
            fg = WHITE
        else:
            bg = (65, 70, 80)      # тёмный — неактивный
            fg = LIGHT_GRAY

        pygame.draw.rect(screen, bg, rect, border_radius=6)
        pygame.draw.rect(screen, (100, 110, 120), rect, 1, border_radius=6)

        # Текст кнопки по центру
        lbl_surf = font_small.render(label, True, fg)
        lx = rect.x + (rect.width  - lbl_surf.get_width())  // 2
        ly = rect.y + (rect.height - lbl_surf.get_height()) // 2
        screen.blit(lbl_surf, (lx, ly))

    #  Кнопка Clear 
    pygame.draw.rect(screen, (200, 60, 60), clear_button, border_radius=8)
    pygame.draw.rect(screen, (240, 100, 100), clear_button, 1, border_radius=8)
    clbl = font.render("Clear", True, WHITE)
    screen.blit(clbl, (clear_button.x + (clear_button.width  - clbl.get_width())  // 2,
                        clear_button.y + (clear_button.height - clbl.get_height()) // 2))

    #  Подпись текущего инструмента и цвета (правый нижний угол) 
    info = font_small.render(
        f"Tool: {current_tool.replace('_',' ')}   Size: {brush_size}",
        True, (150, 160, 170))
    screen.blit(info, (BTN_X0, CANVAS_Y + PANEL_HEIGHT - 20))


#  ОБРАБОТКА КЛИКОВ 

def handle_color_selection(pos):
    """Выбирает цвет из палитры по позиции клика. Возвращает True при попадании."""
    global current_color
    for color, rect in color_palette:
        if rect.collidepoint(pos):
            current_color = color
            return True
    return False


def handle_tool_selection(pos):
    """Выбирает инструмент по позиции клика. Возвращает True при попадании."""
    global current_tool
    for tool, (rect, _) in tool_buttons.items():
        if rect.collidepoint(pos):
            current_tool = tool
            return True
    return False


def handle_clear_button(pos):
    """Очищает холст при клике на кнопку Clear."""
    if clear_button.collidepoint(pos):
        canvas.fill(WHITE)
        return True
    return False


#  ГЛАВНЫЙ ЦИКЛ 
clock   = pygame.time.Clock()
running = True

# Список инструментов, которые рисуются перетаскиванием (не кистью)
SHAPE_TOOLS = {TOOL_RECTANGLE, TOOL_SQUARE, TOOL_CIRCLE,
               TOOL_RIGHT_TRI, TOOL_EQ_TRI, TOOL_RHOMBUS}

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        #  Нажатие кнопки мыши 
        elif event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if event.button == 4:           # колёсико вверх → размер +1
                brush_size = min(brush_size + 1, 30)
            elif event.button == 5:         # колёсико вниз → размер -1
                brush_size = max(brush_size - 1, 1)

            elif event.button == 1:         # левая кнопка
                if pos[1] >= CANVAS_Y:
                    # Клик в зону панели — выбор цвета / инструмента / Clear
                    handle_color_selection(pos)
                    handle_tool_selection(pos)
                    handle_clear_button(pos)
                else:
                    # Клик в зону холста
                    if current_tool in SHAPE_TOOLS:
                        # Запоминаем точку начала для рисования фигуры
                        drawing_shape   = True
                        shape_start_pos = pos
                    else:
                        # Кисть / ластик — начинаем непрерывное рисование
                        last_pos = pos

        #  Отпускание кнопки мыши 
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1 and drawing_shape and shape_start_pos:
                pos = pygame.mouse.get_pos()
                # Фиксируем фигуру на холсте (width=0 → залитая фигура)
                draw_shape(canvas, current_tool,
                           shape_start_pos, pos, current_color, width=0)
                drawing_shape   = False
                shape_start_pos = None

            last_pos = None

        #  Движение мыши 
        elif event.type == MOUSEMOTION:
            pos = pygame.mouse.get_pos()

            if pygame.mouse.get_pressed()[0] and pos[1] < CANVAS_Y:
                # Непрерывное рисование кистью или ластиком
                if current_tool == TOOL_BRUSH and last_pos:
                    draw_line(canvas, current_color, last_pos, pos, brush_size)
                    last_pos = pos
                elif current_tool == TOOL_ERASER and last_pos:
                    draw_line(canvas, WHITE, last_pos, pos, brush_size * 2)
                    last_pos = pos

    #  Отрисовка кадра 

    screen.fill((30, 30, 35))      # фон за пределами холста

    # Холст
    screen.blit(canvas, (0, 0))

    # Предпросмотр фигуры во время перетаскивания (рисуем на screen, не на canvas)
    if drawing_shape and shape_start_pos:
        cur = pygame.mouse.get_pos()
        # Предпросмотр: контур (width=2) поверх холста, чтобы не испортить его
        draw_shape(screen, current_tool,
                   shape_start_pos, cur, current_color, width=2)

    draw_interface()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()