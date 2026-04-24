import pygame
import random
import sys

# КОНСТАНТЫ
CELL        = 24          # размер одной клетки в пикселях
COLS        = 25          # количество колонок игрового поля
ROWS        = 20          # количество строк игрового поля
WALL        = 1           # толщина стены в клетках

WIDTH       = COLS * CELL
HEIGHT      = ROWS * CELL
HUD_HEIGHT  = 50          # высота панели с очками и уровнем
WIN_W       = WIDTH
WIN_H       = HEIGHT + HUD_HEIGHT

BASE_FPS        = 7       # начальная скорость (кадров/сек = шагов змейки)
FPS_PER_LEVEL   = 2       # на сколько fps ускоряется каждый уровень
MAX_FPS         = 25      # максимальная скорость
FOOD_PER_LEVEL  = 4       # сколько еды нужно съесть для перехода на уровень

# ЦВЕТА
C_BG        = ( 10,  14,  20)   # фон поля
C_HUD       = ( 17,  23,  32)   # фон панели HUD
C_WALL      = ( 30,  45,  64)   # цвет стены
C_GRID      = ( 15,  22,  30)   # точки сетки
C_SNAKE_H   = (  0, 229, 255)   # голова змейки
C_SNAKE_B   = (  0, 151, 167)   # тело змейки
C_FOOD      = (255,  64, 129)   # еда
C_TEXT      = (207, 216, 220)   # основной текст
C_DIM       = ( 84, 110, 122)   # приглушённый текст
C_ACCENT    = (  0, 229, 255)   # акцентный цвет
C_ACCENT2   = (255,  64, 129)   # второй акцент (уровень)


# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ — СТЕНЫ
def is_wall(col: int, row: int) -> bool:
    """Возвращает True, если клетка (col, row) является стеной."""
    return col < WALL or row < WALL or col >= COLS - WALL or row >= ROWS - WALL


def free_cells(snake_body: list) -> list:
    """
    Возвращает список всех свободных клеток поля:
    не стена и не занята телом змейки.
    Используется для случайного размещения еды.
    """
    occupied = set((s[0], s[1]) for s in snake_body)
    cells = []
    for r in range(WALL, ROWS - WALL):
        for c in range(WALL, COLS - WALL):
            if (c, r) not in occupied:
                cells.append((c, r))
    return cells


# РАЗМЕЩЕНИЕ ЕДЫ
def place_food(snake_body: list):
    """
    Случайно размещает еду на свободной клетке.
    Гарантирует, что еда не попадёт на стену или тело змейки.
    """
    cells = free_cells(snake_body)
    if not cells:
        return None                          # поле полностью заполнено
    return random.choice(cells)


# ОТРИСОВКА
def draw_grid(surface: pygame.Surface):
    """Рисует маленькие точки сетки на игровом поле."""
    for r in range(WALL, ROWS - WALL):
        for c in range(WALL, COLS - WALL):
            x = c * CELL + CELL // 2
            y = r * CELL + CELL // 2
            pygame.draw.rect(surface, C_GRID, (x - 1, y - 1, 2, 2))


def draw_walls(surface: pygame.Surface):
    """Рисует граничные стены поля."""
    for r in range(ROWS):
        for c in range(COLS):
            if is_wall(c, r):
                pygame.draw.rect(surface, C_WALL,
                                 (c * CELL, r * CELL, CELL, CELL))
    # Внутренняя светящаяся рамка поверх стен
    inner = pygame.Rect(WALL * CELL, WALL * CELL,
                        (COLS - 2 * WALL) * CELL,
                        (ROWS - 2 * WALL) * CELL)
    pygame.draw.rect(surface, (0, 229, 255, 25), inner, 1)


def draw_snake(surface: pygame.Surface, snake_body: list):
    """
    Рисует змейку: голова ярче, тело постепенно темнеет к хвосту.
    """
    total = len(snake_body)
    for i, (col, row) in enumerate(snake_body):
        x = col * CELL + 1
        y = row * CELL + 1
        sz = CELL - 2
        radius = 7 if i == 0 else 4    # голова имеет большее скругление

        # Плавный переход цвета от головы к хвосту
        t = i / max(total - 1, 1)
        r = int(C_SNAKE_H[0] + (C_SNAKE_B[0] - C_SNAKE_H[0]) * t)
        g = int(C_SNAKE_H[1] + (C_SNAKE_B[1] - C_SNAKE_H[1]) * t)
        b = int(C_SNAKE_H[2] + (C_SNAKE_B[2] - C_SNAKE_H[2]) * t)
        color = (r, g, b)

        pygame.draw.rect(surface, color, (x, y, sz, sz), border_radius=radius)

        # Подсветка головы
        if i == 0:
            glow_surf = pygame.Surface((sz + 10, sz + 10), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (0, 229, 255, 60),
                             (0, 0, sz + 10, sz + 10), border_radius=radius + 3)
            surface.blit(glow_surf, (x - 5, y - 5))


def draw_food(surface: pygame.Surface, food):
    """Рисует еду в виде круга с ореолом."""
    if food is None:
        return
    col, row = food
    cx = col * CELL + CELL // 2
    cy = row * CELL + CELL // 2
    radius = CELL // 2 - 3

    # Внешний ореол
    glow = pygame.Surface((CELL * 2, CELL * 2), pygame.SRCALPHA)
    pygame.draw.circle(glow, (255, 64, 129, 50), (CELL, CELL), radius + 7)
    surface.blit(glow, (cx - CELL, cy - CELL))

    # Основной круг еды
    pygame.draw.circle(surface, C_FOOD, (cx, cy), radius)

    # Блик (белое пятно в левом верхнем углу)
    pygame.draw.circle(surface, (255, 255, 255, 150),
                       (cx - radius // 3, cy - radius // 3),
                       max(radius // 3, 2))


def draw_hud(surface: pygame.Surface, font, score: int, level: int, fps: int):
    """
    Рисует нижнюю панель (HUD) с очками, уровнем и текущей скоростью.
    """
    # Фон HUD
    pygame.draw.rect(surface, C_HUD, (0, HEIGHT, WIN_W, HUD_HEIGHT))
    pygame.draw.line(surface, C_WALL, (0, HEIGHT), (WIN_W, HEIGHT), 1)

    # Очки
    sc_lbl = font.render("SCORE", True, C_DIM)
    sc_val = font.render(str(score), True, C_ACCENT)
    surface.blit(sc_lbl, (30, HEIGHT + 8))
    surface.blit(sc_val, (30, HEIGHT + 26))

    # Уровень
    lv_lbl = font.render("LEVEL", True, C_DIM)
    lv_val = font.render(str(level), True, C_ACCENT2)
    surface.blit(lv_lbl, (WIN_W // 2 - 20, HEIGHT + 8))
    surface.blit(lv_val, (WIN_W // 2 - 20, HEIGHT + 26))

    # Скорость
    sp_lbl = font.render("SPEED", True, C_DIM)
    sp_val = font.render(str(fps), True, C_ACCENT)
    surface.blit(sp_lbl, (WIN_W - 90, HEIGHT + 8))
    surface.blit(sp_val, (WIN_W - 90, HEIGHT + 26))


def draw_overlay(surface: pygame.Surface, big_font, font, title: str,
                 sub: str, hint: str):
    """
    Рисует полупрозрачный оверлей по центру экрана
    (начало игры, конец игры, переход уровня, пауза).
    """
    overlay = pygame.Surface((WIN_W, HEIGHT), pygame.SRCALPHA)
    overlay.fill((10, 14, 20, 200))
    surface.blit(overlay, (0, 0))

    # Заголовок
    title_surf = big_font.render(title, True, C_ACCENT)
    tw = title_surf.get_width()
    surface.blit(title_surf, (WIN_W // 2 - tw // 2, HEIGHT // 2 - 60))

    # Подзаголовок
    if sub:
        sub_surf = font.render(sub, True, C_DIM)
        sw = sub_surf.get_width()
        surface.blit(sub_surf, (WIN_W // 2 - sw // 2, HEIGHT // 2))

    # Подсказка
    if hint:
        h_surf = font.render(hint, True, C_TEXT)
        hw = h_surf.get_width()
        surface.blit(h_surf, (WIN_W // 2 - hw // 2, HEIGHT // 2 + 40))


# ОСНОВНОЙ КЛАСС ИГРЫ
class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        pygame.display.set_caption("Snake")

        # Шрифты (встроенные в pygame, не требуют установки)
        self.font     = pygame.font.SysFont("couriernew", 14, bold=True)
        self.big_font = pygame.font.SysFont("couriernew", 42, bold=True)

        self.clock = pygame.time.Clock()
        self.reset()                         # инициализируем игровое состояние

    def reset(self):
        """Сбрасывает все переменные для начала новой игры."""
        mid_col = COLS // 2
        mid_row = ROWS // 2

        # Змейка — список клеток от головы к хвосту
        self.snake = [
            (mid_col,     mid_row),
            (mid_col - 1, mid_row),
            (mid_col - 2, mid_row),
        ]

        self.direction  = (1, 0)    # текущее направление движения (вправо)
        self.next_dir   = (1, 0)    # следующее направление (очередь из ввода)

        self.score      = 0
        self.level      = 1
        self.food_eaten = 0          # счётчик еды на текущем уровне
        self.current_fps = BASE_FPS

        self.food    = place_food(self.snake)   # ТРЕБОВАНИЕ 2: случайная позиция
        self.state   = "start"       # "start" | "running" | "paused" | "levelup" | "gameover"

    # ОБРАБОТКА ВВОДА
    def handle_input(self):
        """Считывает клавиши и события окна."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                self._handle_key(event.key)

    def _handle_key(self, key):
        dx, dy = self.direction

        # Управление змейкой (нельзя развернуться на 180°)
        if key in (pygame.K_UP,    pygame.K_w) and dy != 1:
            self.next_dir = (0, -1)
        elif key in (pygame.K_DOWN,  pygame.K_s) and dy != -1:
            self.next_dir = (0,  1)
        elif key in (pygame.K_LEFT,  pygame.K_a) and dx != 1:
            self.next_dir = (-1, 0)
        elif key in (pygame.K_RIGHT, pygame.K_d) and dx != -1:
            self.next_dir = (1,  0)

        # ENTER / SPACE — переход между состояниями
        elif key in (pygame.K_RETURN, pygame.K_SPACE):
            if self.state == "start":
                self.state = "running"
            elif self.state == "running":
                self.state = "paused"
            elif self.state == "paused":
                self.state = "running"
            elif self.state in ("gameover",):
                self.reset()
                self.state = "running"
            elif self.state == "levelup":
                self.state = "running"

    # ШАГ ЗМЕЙКИ
    def step(self):
        """
        Выполняет один шаг игры: двигает змейку,
        проверяет столкновения, проверяет поедание еды.
        """
        # Применяем новое направление
        self.direction = self.next_dir
        dx, dy = self.direction

        head_col, head_row = self.snake[0]
        new_head = (head_col + dx, head_row + dy)

        # --- ТРЕБОВАНИЕ 1: Проверка столкновения со стеной ---
        if is_wall(new_head[0], new_head[1]):
            self.state = "gameover"
            return

        # --- Проверка столкновения с собственным телом ---
        # Хвост ещё не удалён, поэтому проверяем до последнего элемента
        if new_head in self.snake[:-1]:
            self.state = "gameover"
            return

        # Добавляем новую голову
        self.snake.insert(0, new_head)

        # Проверяем, съедена ли еда
        if new_head == self.food:
            # Змейка вырастает (хвост НЕ удаляем)
            self.score      += self.level * 10    # очки зависят от уровня
            self.food_eaten += 1

            # ТРЕБОВАНИЕ 2: новая случайная позиция еды
            self.food = place_food(self.snake)

            # ТРЕБОВАНИЕ 3: переход на следующий уровень
            if self.food_eaten >= FOOD_PER_LEVEL:
                self._advance_level()
        else:
            # Еда не съедена → удаляем хвост (длина не меняется)
            self.snake.pop()

    # ПЕРЕХОД НА НОВЫЙ УРОВЕНЬ
    def _advance_level(self):
        """
        Увеличивает уровень, сбрасывает счётчик еды,
        повышает скорость и показывает экран уровня.
        """
        self.level      += 1
        self.food_eaten  = 0

        # ТРЕБОВАНИЕ 4: увеличение скорости
        self.current_fps = min(BASE_FPS + (self.level - 1) * FPS_PER_LEVEL,
                               MAX_FPS)

        self.state = "levelup"

    # ОТРИСОВКА КАДРА
    def draw(self):
        """Собирает и отрисовывает один кадр игры."""
        self.screen.fill(C_BG)

        draw_grid(self.screen)
        draw_walls(self.screen)
        draw_food(self.screen, self.food)
        draw_snake(self.screen, self.snake)

        # ТРЕБОВАНИЕ 5: HUD с очками и уровнем
        draw_hud(self.screen, self.font,
                 self.score, self.level, self.current_fps)

        # Оверлей в зависимости от состояния игры
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

    # ГЛАВНЫЙ ЦИКЛ
    def run(self):
        """Запускает основной игровой цикл."""
        while True:
            self.handle_input()

            # Шаг игры только в режиме "running"
            if self.state == "running":
                self.step()

            self.draw()

            # Скорость: зависит от текущего уровня (ТРЕБОВАНИЕ 4)
            if self.state == "running":
                self.clock.tick(self.current_fps)
            else:
                self.clock.tick(30)          # в меню/паузе — 30 fps достаточно


# ТОЧКА ВХОДА
if __name__ == "__main__":
    game = SnakeGame()
    game.run()