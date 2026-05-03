import pygame
import random

FOOD_NORMAL = "normal"
FOOD_BONUS = "bonus"
FOOD_POISON = "poison"

PU_SPEED = "speed"
PU_SLOW = "slow"
PU_SHIELD = "shield"

FOOD_POINTS = {FOOD_NORMAL: 1, FOOD_BONUS: 3, FOOD_POISON: 0}

FOOD_COLORS = {
    FOOD_NORMAL: (220, 50, 50),
    FOOD_BONUS:  (255, 165, 0),
    FOOD_POISON: (100, 0, 0),
}

PU_COLORS = {
    PU_SPEED:  (0, 200, 255),
    PU_SLOW:   (180, 0, 255),
    PU_SHIELD: (255, 215, 0),
}


class Game:
    def __init__(self, cols, rows, base_speed, food_per_level, snake_color):
        self.cols = cols
        self.rows = rows
        self.base_speed = base_speed
        self.food_per_level = food_per_level
        self.snake_color = snake_color
        self.reset()

    def reset(self):
        cx, cy = self.cols // 2, self.rows // 2
        self.snake = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.dir = (1, 0)
        self.next_dir = (1, 0)
        self.score = 0
        self.level = 1
        self.eaten = 0
        self.speed = self.base_speed
        self.obstacles = []
        self.foods = []
        self.powerup = None
        self.effect = None
        self.effect_end = 0
        self.shield = False
        self.over = False
        self._spawn_food()

    def _occupied(self):
        s = set(self.snake) | set(self.obstacles)
        for f in self.foods:
            s.add(f["pos"])
        if self.powerup:
            s.add(self.powerup["pos"])
        return s

    def _free_cells(self):
        occ = self._occupied()
        return [
            (x, y)
            for x in range(self.cols)
            for y in range(self.rows)
            if (x, y) not in occ
        ]

    def _spawn_food(self):
        free = self._free_cells()
        if not free:
            return
        pos = random.choice(free)
        kind = random.choices(
            [FOOD_NORMAL, FOOD_BONUS, FOOD_POISON],
            weights=[60, 25, 15]
        )[0]
        self.foods.append({
            "pos": pos,
            "kind": kind,
            "born": pygame.time.get_ticks(),
            "ttl": 8000 if kind == FOOD_BONUS else None,
        })

    def _try_spawn_powerup(self):
        if self.powerup is not None:
            return
        if random.random() < 0.4:
            free = self._free_cells()
            if free:
                self.powerup = {
                    "pos": random.choice(free),
                    "kind": random.choice([PU_SPEED, PU_SLOW, PU_SHIELD]),
                    "born": pygame.time.get_ticks(),
                }

    def _place_obstacles(self):
        head = self.snake[0]
        safe = {
            (head[0] + dx, head[1] + dy)
            for dx in range(-5, 6)
            for dy in range(-5, 6)
        }
        safe |= set(self.snake)
        count = min(self.level * 3, 24)
        placed = []
        attempts = 0
        while len(placed) < count and attempts < 2000:
            x = random.randint(0, self.cols - 1)
            y = random.randint(0, self.rows - 1)
            if (x, y) not in safe and (x, y) not in placed:
                placed.append((x, y))
            attempts += 1
        self.obstacles = placed

    def _calc_base_speed(self):
        return self.base_speed + (self.level - 1) * 2

    def set_dir(self, d):
        if d[0] + self.dir[0] != 0 or d[1] + self.dir[1] != 0:
            self.next_dir = d

    def update(self):
        if self.over:
            return

        now = pygame.time.get_ticks()
        self.dir = self.next_dir
        hx, hy = self.snake[0]
        nx, ny = hx + self.dir[0], hy + self.dir[1]

        wall_hit = not (0 <= nx < self.cols and 0 <= ny < self.rows)
        body_hit = (nx, ny) in self.snake[:-1]
        obs_hit = (nx, ny) in self.obstacles

        if wall_hit or body_hit or obs_hit:
            if self.shield:
                self.shield = False
                return
            self.over = True
            return

        self.snake.insert(0, (nx, ny))

        eaten = next((f for f in self.foods if f["pos"] == (nx, ny)), None)
        if eaten:
            self.foods.remove(eaten)
            if eaten["kind"] == FOOD_POISON:
                self.snake.pop()
                for _ in range(2):
                    if len(self.snake) > 1:
                        self.snake.pop()
                if len(self.snake) <= 1:
                    self.over = True
                    return
            else:
                self.score += FOOD_POINTS[eaten["kind"]]
                self.eaten += 1
                if self.eaten % self.food_per_level == 0:
                    self._level_up()
            self._spawn_food()
            self._try_spawn_powerup()
        else:
            self.snake.pop()

        if self.powerup and self.powerup["pos"] == (nx, ny):
            self._apply_powerup(self.powerup["kind"], now)
            self.powerup = None

        if self.powerup and now - self.powerup["born"] > 8000:
            self.powerup = None

        self.foods = [
            f for f in self.foods
            if f["ttl"] is None or now - f["born"] < f["ttl"]
        ]
        if not self.foods:
            self._spawn_food()

        if self.effect and now > self.effect_end:
            self.effect = None
            self.speed = self._calc_base_speed()

    def _level_up(self):
        self.level += 1
        self.speed = self._calc_base_speed()
        if self.level >= 3:
            self._place_obstacles()

    def _apply_powerup(self, kind, now):
        if kind == PU_SHIELD:
            self.shield = True
            return
        self.effect = kind
        self.effect_end = now + 5000
        base = self._calc_base_speed()
        if kind == PU_SPEED:
            self.speed = base + 6
        else:
            self.speed = max(2, base - 4)

    def draw(self, surf, show_grid, g):
        if show_grid:
            for x in range(0, self.cols * g, g):
                pygame.draw.line(surf, (28, 28, 38), (x, 0), (x, self.rows * g))
            for y in range(0, self.rows * g, g):
                pygame.draw.line(surf, (28, 28, 38), (0, y), (self.cols * g, y))

        for ox, oy in self.obstacles:
            pygame.draw.rect(surf, (90, 70, 50), (ox * g, oy * g, g, g))
            pygame.draw.rect(surf, (60, 45, 30), (ox * g, oy * g, g, g), 2)

        for f in self.foods:
            color = FOOD_COLORS[f["kind"]]
            pygame.draw.rect(
                surf, color,
                (f["pos"][0] * g + 3, f["pos"][1] * g + 3, g - 6, g - 6)
            )

        if self.powerup:
            col = PU_COLORS[self.powerup["kind"]]
            px = self.powerup["pos"][0] * g + g // 2
            py = self.powerup["pos"][1] * g + g // 2
            r = g // 2 - 2
            pygame.draw.polygon(surf, col, [
                (px, py - r),
                (px + r, py + r),
                (px - r, py + r),
            ])

        head_color = tuple(min(c + 70, 255) for c in self.snake_color)
        for i, (sx, sy) in enumerate(self.snake):
            color = head_color if i == 0 else self.snake_color
            pygame.draw.rect(surf, color, (sx * g + 1, sy * g + 1, g - 2, g - 2))
            if i == 0:
                pygame.draw.rect(surf, (255, 255, 255), (sx * g + 1, sy * g + 1, g - 2, g - 2), 1)