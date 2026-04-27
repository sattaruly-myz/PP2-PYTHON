import pygame
import random
import sys
import math

#  КОНСТАНТЫ ПОЛЯ 
CELL        = 24          # размер одной клетки в пикселях
COLS        = 25          # количество колонок игрового поля
ROWS        = 20          # количество строк игрового поля
WALL        = 1           # толщина стены в клетках

WIDTH       = COLS * CELL
HEIGHT      = ROWS * CELL
HUD_HEIGHT  = 50          # высота панели с очками и уровнем
WIN_W       = WIDTH
WIN_H       = HEIGHT + HUD_HEIGHT

#  СКОРОСТЬ 
BASE_FPS        = 7       # начальная скорость (кадров/сек = шагов змейки)
FPS_PER_LEVEL   = 2       # на сколько fps ускоряется каждый уровень
MAX_FPS         = 25      # максимальная скорость
FOOD_PER_LEVEL  = 4       # сколько еды нужно съесть для перехода на уровень

#  НАСТРОЙКИ ЕДЫ 
MAX_FOODS          = 3    # максимум еды на поле одновременно
FOOD_SPAWN_FRAMES  = 30   # каждые N игровых шагов появляется новая единица еды

# Таблица типов еды: (вес, цвет_основной, цвет_ореола, кадров_жизни, вероятность)
# Вес влияет на количество даваемых очков: очки = weight * level * 10
# Таймер задан в игровых шагах (не в кадрах), чтобы не зависеть от fps
FOOD_TYPES = [
    {"weight": 1, "color": (255,  64, 129), "glow": (255,  64, 129,  50),
     "steps": 30, "label": "●", "prob": 60},   # обычная — розовая, 30 шагов
    {"weight": 3, "color": (255, 165,   0), "glow": (255, 165,   0,  50),
     "steps": 20, "label": "◆", "prob": 30},   # редкая  — оранжевая, 20 шагов
    {"weight": 5, "color": (  0, 255, 180), "glow": (  0, 255, 180,  50),
     "steps": 12, "label": "★", "prob": 10},   # эпик    — зелёная,  12 шагов
]
FOOD_PROBS = [t["prob"] for t in FOOD_TYPES]  # список вероятностей для random.choices

#  ЦВЕТОВАЯ СХЕМА 
C_BG        = ( 10,  14,  20)
C_HUD       = ( 17,  23,  32)
C_WALL      = ( 30,  45,  64)
C_GRID      = ( 15,  22,  30)
C_SNAKE_H   = (  0, 229, 255)
C_SNAKE_B   = (  0, 151, 167)
C_TEXT      = (207, 216, 220)
C_DIM       = ( 84, 110, 122)
C_ACCENT    = (  0, 229, 255)
C_ACCENT2   = (255,  64, 129)


#  ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ — ПОЛЕ 

def is_wall(col: int, row: int) -> bool:
    """Возвращает True, если клетка (col, row) является граничной стеной."""
    return col < WALL or row < WALL or col >= COLS - WALL or row >= ROWS - WALL


def free_cells(snake_body: list, food_list: list) -> list:
    """
    Возвращает список всех свободных клеток (не стена, не тело змейки,
    не занята уже существующей едой).
    Используется при размещении новой единицы еды.
    """
    occupied = set((s[0], s[1]) for s in snake_body)
    occupied |= set(f["pos"] for f in food_list)    # добавляем позиции еды
    cells = []
    for r in range(WALL, ROWS - WALL):
        for c in range(WALL, COLS - WALL):
            if (c, r) not in occupied:
                cells.append((c, r))
    return cells


#  СОЗДАНИЕ ЕДИНИЦЫ ЕДЫ 

def create_food(snake_body: list, food_list: list):
    """
    Случайно выбирает тип еды (по вероятностям из FOOD_TYPES)
    и размещает её на свободной клетке.
    Возвращает словарь с данными о еде или None, если места нет.
    """
    cells = free_cells(snake_body, food_list)
    if not cells:
        return None   # поле полностью заполнено

    pos  = random.choice(cells)
    ftype = random.choices(FOOD_TYPES, weights=FOOD_PROBS, k=1)[0]

    return {
        "pos":       pos,
        "weight":    ftype["weight"],
        "color":     ftype["color"],
        "glow":      ftype["glow"],
        "steps":     ftype["steps"],      # оставшееся число игровых шагов
        "max_steps": ftype["steps"],      # исходное число шагов (для % таймера)
    }


#  ОТРИСОВКА 

def draw_grid(surface: pygame.Surface):
    """Рисует маленькие точки сетки на игровом поле."""
    for r in range(WALL, ROWS - WALL):
        for c in range(WALL, COLS - WALL):
            x = c * CELL + CELL // 2
            y = r * CELL + CELL // 2
            pygame.draw.rect(surface, C_GRID, (x - 1, y - 1, 2, 2))


def draw_walls(surface: pygame.Surface):
    """Рисует граничные стены и светящуюся внутреннюю рамку."""
    for r in range(ROWS):
        for c in range(COLS):
            if is_wall(c, r):
                pygame.draw.rect(surface, C_WALL,
                                 (c * CELL, r * CELL, CELL, CELL))
    inner = pygame.Rect(WALL * CELL, WALL * CELL,
                        (COLS - 2 * WALL) * CELL,
                        (ROWS - 2 * WALL) * CELL)
    pygame.draw.rect(surface, (0, 229, 255, 25), inner, 1)


def draw_snake(surface: pygame.Surface, snake_body: list):
    """
    Рисует змейку с плавным переходом цвета от головы (голубой) к хвосту (тёмный).
    Голова имеет большее скругление углов и подсветку (glow).
    """
    total = len(snake_body)
    for i, (col, row) in enumerate(snake_body):
        x  = col * CELL + 1
        y  = row * CELL + 1
        sz = CELL - 2
        radius = 7 if i == 0 else 4

        # Интерполяция цвета голова → хвост
        t = i / max(total - 1, 1)
        r = int(C_SNAKE_H[0] + (C_SNAKE_B[0] - C_SNAKE_H[0]) * t)
        g = int(C_SNAKE_H[1] + (C_SNAKE_B[1] - C_SNAKE_H[1]) * t)
        b = int(C_SNAKE_H[2] + (C_SNAKE_B[2] - C_SNAKE_H[2]) * t)

        pygame.draw.rect(surface, (r, g, b), (x, y, sz, sz),
                         border_radius=radius)

        # Подсветка головы
        if i == 0:
            glow_surf = pygame.Surface((sz + 10, sz + 10), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (0, 229, 255, 60),
                             (0, 0, sz + 10, sz + 10), border_radius=radius + 3)
            surface.blit(glow_surf, (x - 5, y - 5))


def draw_food_list(surface: pygame.Surface, food_list: list, font_small):
    """
    Рисует все активные единицы еды.

    Для каждой еды отображается:
    - Внешний ореол (glow) из FOOD_TYPES
    - Основной круг с цветом типа
    - Блик в верхнем углу
    - Надпись веса (1 / 3 / 5) по центру
    - Дуговой таймер: белая дуга убывает по часовой стрелке пропорционально
      оставшемуся времени (steps / max_steps)
    """
    for food in food_list:
        col, row = food["pos"]
        cx = col * CELL + CELL // 2
        cy = row * CELL + CELL // 2
        radius = CELL // 2 - 3

        #  Ореол 
        glow = pygame.Surface((CELL * 2, CELL * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow, food["glow"], (CELL, CELL), radius + 7)
        surface.blit(glow, (cx - CELL, cy - CELL))

        #  Основной круг 
        # Цвет тускнеет, когда еда скоро исчезнет (последние 30% времени)
        ratio     = food["steps"] / food["max_steps"]   # 1.0 → 0.0
        fade      = max(0.4, ratio)                      # минимум 40% яркости
        faded_col = tuple(int(c * fade) for c in food["color"])
        pygame.draw.circle(surface, faded_col, (cx, cy), radius)

        #  Блик 
        pygame.draw.circle(surface, (255, 255, 255),
                           (cx - radius // 3, cy - radius // 3),
                           max(radius // 3, 2))

        #  Вес по центру 
        lbl = font_small.render(str(food["weight"]), True, (255, 255, 255))
        surface.blit(lbl, (cx - lbl.get_width()  // 2,
                           cy - lbl.get_height() // 2))

        #  Дуговой таймер 
        # Рисуем белую дугу вокруг еды, убывающую с 360° до 0°
        arc_radius  = radius + 5
        arc_rect    = pygame.Rect(cx - arc_radius, cy - arc_radius,
                                  arc_radius * 2,  arc_radius * 2)
        # pygame.draw.arc идёт против часовой — конвертируем угол
        start_angle = math.pi / 2                         # 12 часов = 90°
        end_angle   = start_angle + 2 * math.pi * ratio   # убывает по мере таймера

        # Цвет дуги: зелёный при большом запасе времени, красный — при малом
        arc_color = (
            int(255 * (1 - ratio)),   # R растёт при убывании
            int(255 * ratio),          # G убывает
            50
        )
        if arc_radius > 0 and ratio > 0:
            pygame.draw.arc(surface, arc_color, arc_rect,
                            start_angle, end_angle, 2)


def draw_hud(surface: pygame.Surface, font, score: int, level: int, fps: int):
    """
    Рисует нижнюю панель HUD:
    слева — SCORE, по центру — LEVEL, справа — SPEED.
    """
    pygame.draw.rect(surface, C_HUD, (0, HEIGHT, WIN_W, HUD_HEIGHT))
    pygame.draw.line(surface, C_WALL, (0, HEIGHT), (WIN_W, HEIGHT), 1)

    for label, value, color, x in [
        ("SCORE", str(score),  C_ACCENT,  30),
        ("LEVEL", str(level),  C_ACCENT2, WIN_W // 2 - 20),
        ("SPEED", str(fps),    C_ACCENT,  WIN_W - 90),
    ]:
        surface.blit(font.render(label, True, C_DIM),   (x, HEIGHT + 8))
        surface.blit(font.render(value, True, color),   (x, HEIGHT + 26))


def draw_overlay(surface: pygame.Surface, big_font, font,
                 title: str, sub: str, hint: str):
    """
    Рисует полупрозрачный оверлей (начало, пауза, конец игры, смена уровня).
    Три строки: заголовок, подзаголовок, подсказка.
    """
    overlay = pygame.Surface((WIN_W, HEIGHT), pygame.SRCALPHA)
    overlay.fill((10, 14, 20, 200))
    surface.blit(overlay, (0, 0))

    for text, fnt, color, dy in [
        (title, big_font, C_ACCENT,  -60),
        (sub,   font,     C_DIM,       0),
        (hint,  font,     C_TEXT,     40),
    ]:
        if not text:
            continue
        surf = fnt.render(text, True, color)
        surface.blit(surf, (WIN_W // 2 - surf.get_width() // 2,
                            HEIGHT // 2 + dy))


#  ОСНОВНОЙ КЛАСС ИГРЫ 

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        pygame.display.set_caption("Snake")

        self.font       = pygame.font.SysFont("couriernew", 14, bold=True)
        self.font_small = pygame.font.SysFont("couriernew", 11, bold=True)
        self.big_font   = pygame.font.SysFont("couriernew", 42, bold=True)

        self.clock = pygame.time.Clock()
        self.reset()

    #  Сброс состояния 
    def reset(self):
        """Инициализирует все переменные для новой игры."""
        mid_col = COLS // 2
        mid_row = ROWS // 2

        # Змейка — список клеток [(col, row), ...] от головы к хвосту
        self.snake = [
            (mid_col,     mid_row),
            (mid_col - 1, mid_row),
            (mid_col - 2, mid_row),
        ]

        self.direction   = (1, 0)    # текущее направление
        self.next_dir    = (1, 0)    # направление в следующем шаге

        self.score       = 0
        self.level       = 1
        self.food_eaten  = 0         # съедено на текущем уровне
        self.current_fps = BASE_FPS

        # Счётчик шагов для спавна новой еды
        self.spawn_counter = 0

        # Список активных единиц еды (каждая — словарь из create_food)
        self.food_list = []
        # Спавним начальную еду
        for _ in range(2):
            f = create_food(self.snake, self.food_list)
            if f:
                self.food_list.append(f)

        # Состояние: "start" | "running" | "paused" | "levelup" | "gameover"
        self.state = "start"

    #  Обработка ввода 
    def handle_input(self):
        """Обрабатывает события pygame: выход, нажатия клавиш."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self._handle_key(event.key)

    def _handle_key(self, key):
        """Маршрутизирует нажатие клавиши: управление или смена состояния."""
        dx, dy = self.direction

        # Управление змейкой (разворот на 180° запрещён)
        dirs = {
            pygame.K_UP:    (( 0, -1), dy !=  1),
            pygame.K_w:     (( 0, -1), dy !=  1),
            pygame.K_DOWN:  (( 0,  1), dy != -1),
            pygame.K_s:     (( 0,  1), dy != -1),
            pygame.K_LEFT:  ((-1,  0), dx !=  1),
            pygame.K_a:     ((-1,  0), dx !=  1),
            pygame.K_RIGHT: (( 1,  0), dx != -1),
            pygame.K_d:     (( 1,  0), dx != -1),
        }
        if key in dirs:
            new_dir, allowed = dirs[key]
            if allowed:
                self.next_dir = new_dir
            return

        # Пробел / Enter управляют состоянием игры
        if key in (pygame.K_RETURN, pygame.K_SPACE):
            transitions = {
                "start":    "running",
                "paused":   "running",
                "levelup":  "running",
            }
            if self.state in transitions:
                self.state = transitions[self.state]
            elif self.state == "running":
                self.state = "paused"
            elif self.state == "gameover":
                self.reset()
                self.state = "running"

    #  Один шаг игры 
    def step(self):
        """
        Выполняет один игровой шаг:
        1. Двигает змейку.
        2. Проверяет столкновения.
        3. Обрабатывает поедание еды.
        4. Уменьшает таймеры еды, удаляет просроченную.
        5. Спавнит новую еду по расписанию.
        """
        # Применяем направление из очереди
        self.direction = self.next_dir
        dx, dy = self.direction
        head_col, head_row = self.snake[0]
        new_head = (head_col + dx, head_row + dy)

        #  Столкновение со стеной 
        if is_wall(new_head[0], new_head[1]):
            self.state = "gameover"
            return

        #  Столкновение с собственным телом 
        if new_head in self.snake[:-1]:
            self.state = "gameover"
            return

        self.snake.insert(0, new_head)   # добавляем новую голову

        #  Проверяем, съедена ли какая-либо еда 
        eaten = None
        for food in self.food_list:
            if new_head == food["pos"]:
                eaten = food
                break

        if eaten:
            # Начисляем очки: вес × уровень × 10
            self.score      += eaten["weight"] * self.level * 10
            self.food_eaten += 1
            self.food_list.remove(eaten)   # убираем съеденную еду

            # Переход на новый уровень
            if self.food_eaten >= FOOD_PER_LEVEL:
                self._advance_level()
        else:
            # Еда не съедена — хвост отрезается (длина не меняется)
            self.snake.pop()

        #  Таймеры еды: уменьшаем счётчик шагов 
        for food in self.food_list[:]:    # итерация по копии
            food["steps"] -= 1
            if food["steps"] <= 0:
                self.food_list.remove(food)   # еда истекла — убираем с поля

        #  Спавн новой еды по расписанию 
        self.spawn_counter += 1
        if (self.spawn_counter >= FOOD_SPAWN_FRAMES
                and len(self.food_list) < MAX_FOODS):
            self.spawn_counter = 0
            new_food = create_food(self.snake, self.food_list)
            if new_food:
                self.food_list.append(new_food)

    #  Переход на следующий уровень 
    def _advance_level(self):
        """Повышает уровень, сбрасывает счётчик еды, ускоряет игру."""
        self.level      += 1
        self.food_eaten  = 0
        self.current_fps = min(BASE_FPS + (self.level - 1) * FPS_PER_LEVEL,
                               MAX_FPS)
        self.state = "levelup"

    #  Отрисовка 
    def draw(self):
        """Собирает и отрисовывает полный кадр игры."""
        self.screen.fill(C_BG)

        draw_grid(self.screen)
        draw_walls(self.screen)
        draw_food_list(self.screen, self.food_list, self.font_small)
        draw_snake(self.screen, self.snake)
        draw_hud(self.screen, self.font,
                 self.score, self.level, self.current_fps)

        # Оверлеи для нерабочих состояний
        if self.state == "start":
            draw_overlay(self.screen, self.big_font, self.font,
                         "SNAKE",
                         f"Level {self.level}  |  Eat {FOOD_PER_LEVEL} foods to advance",
                         "PRESS ENTER or SPACE to start")
        elif self.state == "paused":
            draw_overlay(self.screen, self.big_font, self.font,
                         "PAUSED", "", "PRESS SPACE to resume")
        elif self.state == "levelup":
            draw_overlay(self.screen, self.big_font, self.font,
                         f"LEVEL {self.level}!",
                         f"Speed: {self.current_fps} fps  |  Score: {self.score}",
                         "PRESS ENTER or SPACE to continue")
        elif self.state == "gameover":
            draw_overlay(self.screen, self.big_font, self.font,
                         "GAME OVER",
                         f"Score: {self.score}  |  Level: {self.level}",
                         "PRESS ENTER or SPACE to restart")

        pygame.display.flip()

    #  Главный цикл 
    def run(self):
        """Запускает основной игровой цикл."""
        while True:
            self.handle_input()

            if self.state == "running":
                self.step()

            self.draw()

            # Скорость тика зависит от уровня; в меню/паузе 30 fps
            self.clock.tick(self.current_fps if self.state == "running" else 30)


#  ТОЧКА ВХОДА 
if __name__ == "__main__":
    game = SnakeGame()
    game.run()