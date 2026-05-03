import pygame
import random
import math

W, H = 600, 750

ROAD_LEFT  = 80
ROAD_RIGHT = 520
ROAD_W     = ROAD_RIGHT - ROAD_LEFT
LANE_COUNT = 4
LANE_W     = ROAD_W // LANE_COUNT
LANE_CX    = [ROAD_LEFT + LANE_W * i + LANE_W // 2 for i in range(LANE_COUNT)]

CAR_COLORS = {
    'red':    (215, 50,  50),
    'blue':   (50,  100, 220),
    'green':  (50,  185, 80),
    'yellow': (215, 195, 30),
}

DIFF = {
    'easy':   {'speed': 4.0, 'traffic': 130, 'obstacle': 220, 'coin': 65},
    'normal': {'speed': 6.0, 'traffic': 85,  'obstacle': 145, 'coin': 52},
    'hard':   {'speed': 9.0, 'traffic': 52,  'obstacle': 90,  'coin': 42},
}

PU_COLOR = {'nitro': (50, 220, 80), 'shield': (60, 150, 255), 'repair': (255, 175, 30)}

COIN_POOL = [
    {'color': (175, 100, 45), 'value': 1,  'r': 10, 'w': 60},
    {'color': (180, 180, 180),'value': 3,  'r': 12, 'w': 30},
    {'color': (255, 210, 0),  'value': 5,  'r': 14, 'w': 10},
]

_F_SM  = None
_F_MED = None
_F_PU  = None


def _init_fonts():
    global _F_SM, _F_MED, _F_PU
    if _F_SM is None:
        _F_SM  = pygame.font.SysFont('Arial', 13, bold=True)
        _F_MED = pygame.font.SysFont('Arial', 18)
        _F_PU  = pygame.font.SysFont('Arial', 16, bold=True)


def _draw_car(surf, cx, cy, w, h, body, detail=(210, 210, 210)):
    pygame.draw.rect(surf, body, (cx - w//2, cy - h//2, w, h), border_radius=6)
    pygame.draw.rect(surf, detail, (cx - w//2 + 4, cy - h//2 + 7,  w - 8, 13), border_radius=3)
    pygame.draw.rect(surf, detail, (cx - w//2 + 4, cy + h//2 - 20, w - 8, 12), border_radius=3)
    wc = (20, 20, 20)
    for wx, wy in [(-w//2 - 4, -h//2 + 7), (w//2 - 4, -h//2 + 7),
                   (-w//2 - 4, h//2 - 20),  (w//2 - 4, h//2 - 20)]:
        pygame.draw.rect(surf, wc, (cx + wx, cy + wy, 8, 13), border_radius=2)


class Road:
    DASH_H   = 38
    DASH_GAP = 38

    def __init__(self, speed):
        self.speed  = speed
        self.offset = 0
        self.total  = self.DASH_H + self.DASH_GAP
        self.slow_zones   = []
        self.nitro_strips = []
        self._slow_t  = random.randint(180, 320)
        self._nitro_t = random.randint(280, 480)
        self._alpha_surf = pygame.Surface((LANE_W, 1), pygame.SRCALPHA)

    def update(self):
        self.offset = (self.offset + self.speed) % self.total

        self._slow_t -= 1
        if self._slow_t <= 0:
            self.slow_zones.append({'lane': random.randint(0, LANE_COUNT - 1), 'y': -90, 'h': 70})
            self._slow_t = random.randint(200, 380)

        self._nitro_t -= 1
        if self._nitro_t <= 0:
            self.nitro_strips.append({'lane': random.randint(0, LANE_COUNT - 1), 'y': -50, 'h': 32})
            self._nitro_t = random.randint(320, 560)

        for z in self.slow_zones:
            z['y'] += self.speed
        for n in self.nitro_strips:
            n['y'] += self.speed

        self.slow_zones   = [z for z in self.slow_zones   if z['y'] < H + 120]
        self.nitro_strips = [n for n in self.nitro_strips if n['y'] < H + 80]

    def in_slow(self, lane, py):
        return any(z['lane'] == lane and z['y'] < py < z['y'] + z['h'] for z in self.slow_zones)

    def in_nitro(self, lane, py):
        return any(n['lane'] == lane and n['y'] < py < n['y'] + n['h'] for n in self.nitro_strips)

    def draw(self, surf):
        pygame.draw.rect(surf, (30, 95, 30),  (0, 0, ROAD_LEFT, H))
        pygame.draw.rect(surf, (30, 95, 30),  (ROAD_RIGHT, 0, W - ROAD_RIGHT, H))
        pygame.draw.rect(surf, (48, 48, 54),  (ROAD_LEFT, 0, ROAD_W, H))

        for z in self.slow_zones:
            x = ROAD_LEFT + z['lane'] * LANE_W
            s = pygame.Surface((LANE_W, z['h']), pygame.SRCALPHA)
            s.fill((255, 120, 0, 70))
            surf.blit(s, (x, int(z['y'])))
            for i in range(0, int(z['h']), 12):
                if (i // 12) % 2 == 0:
                    pygame.draw.rect(surf, (200, 90, 0), (x, int(z['y']) + i, LANE_W, 6))

        for n in self.nitro_strips:
            x = ROAD_LEFT + n['lane'] * LANE_W
            s = pygame.Surface((LANE_W, n['h']), pygame.SRCALPHA)
            s.fill((0, 255, 100, 90))
            surf.blit(s, (x, int(n['y'])))

        for i in range(1, LANE_COUNT):
            x = ROAD_LEFT + i * LANE_W
            y = -self.offset
            while y < H:
                pygame.draw.rect(surf, (190, 190, 190), (x - 1, int(y), 2, self.DASH_H))
                y += self.total

        pygame.draw.rect(surf, (215, 195, 0), (ROAD_LEFT,     0, 4, H))
        pygame.draw.rect(surf, (215, 195, 0), (ROAD_RIGHT - 4, 0, 4, H))


class Player:
    CW, CH = 40, 70

    def __init__(self, color):
        self.lane    = 1
        self.x       = float(LANE_CX[self.lane])
        self.y       = float(H - 120)
        self.tx      = self.x
        self.color   = color
        self.smult   = 1.0
        self.nitro_t = 0
        self.shield  = False
        self.s_flash = 0

    def move(self, d):
        nl = self.lane + d
        if 0 <= nl < LANE_COUNT:
            self.lane = nl
            self.tx = float(LANE_CX[self.lane])

    def update(self):
        dx = self.tx - self.x
        self.x = self.tx if abs(dx) < 1 else self.x + dx * 0.22
        if self.nitro_t > 0:
            self.nitro_t -= 1
            if self.nitro_t == 0:
                self.smult = 1.0
        if self.s_flash > 0:
            self.s_flash -= 1

    def rect(self):
        return pygame.Rect(int(self.x) - self.CW//2, int(self.y) - self.CH//2, self.CW, self.CH)

    def draw(self, surf):
        _draw_car(surf, int(self.x), int(self.y), self.CW, self.CH, self.color)
        if self.shield:
            show = self.s_flash == 0 or (self.s_flash % 20 < 10)
            if show:
                s = pygame.Surface((self.CW + 18, self.CH + 18), pygame.SRCALPHA)
                pygame.draw.ellipse(s, (60, 160, 255, 75),  s.get_rect())
                pygame.draw.ellipse(s, (120, 200, 255, 180), s.get_rect(), 3)
                surf.blit(s, (int(self.x) - self.CW//2 - 9, int(self.y) - self.CH//2 - 9))
        if self.nitro_t > 0:
            for _ in range(4):
                px = int(self.x) + random.randint(-9, 9)
                py = int(self.y) + self.CH//2 + random.randint(4, 22)
                pygame.draw.circle(surf, (255, random.randint(80, 180), 0), (px, py), random.randint(3, 8))


class TrafficCar:
    CW, CH = 40, 70
    COLS = [(195,75,75),(75,75,195),(75,190,75),(190,190,75),(155,75,195),(75,175,175)]

    def __init__(self, road_speed):
        self.lane  = random.randint(0, LANE_COUNT - 1)
        self.x     = float(LANE_CX[self.lane])
        self.y     = float(-self.CH)
        self.speed = road_speed * (0.25 + random.uniform(0, 0.2))
        self.color = random.choice(self.COLS)

    def update(self, road_speed):
        self.y += road_speed * 0.45 + self.speed

    def rect(self):
        return pygame.Rect(int(self.x) - self.CW//2, int(self.y) - self.CH//2, self.CW, self.CH)

    def gone(self):
        return self.y > H + self.CH

    def draw(self, surf):
        _draw_car(surf, int(self.x), int(self.y), self.CW, self.CH, self.color)


class Obstacle:
    def __init__(self, kind, road_speed):
        self.kind  = kind
        self.lane  = random.randint(0, LANE_COUNT - 1)
        self.x     = LANE_CX[self.lane]
        self.y     = float(-40)
        self.speed = road_speed
        self.w, self.h = 52, 28

    def update(self, road_speed):
        self.y += road_speed

    def rect(self):
        return pygame.Rect(int(self.x) - self.w//2, int(self.y) - self.h//2, self.w, self.h)

    def gone(self):
        return self.y > H + self.h

    def draw(self, surf):
        cx, cy = int(self.x), int(self.y)
        if self.kind == 'oil':
            pygame.draw.ellipse(surf, (18, 18, 38), (cx-26, cy-14, 52, 28))
            pygame.draw.ellipse(surf, (38, 0, 75),  (cx-21, cy-11, 42, 22))
            for i, c in enumerate([(255,0,80),(0,200,255),(120,0,255)]):
                s = pygame.Surface((36 - i*6, 16 - i*3), pygame.SRCALPHA)
                pygame.draw.ellipse(s, (*c, 55), s.get_rect())
                surf.blit(s, (cx - 18 + i*3, cy - 8 + i*1))
        elif self.kind == 'pothole':
            pygame.draw.ellipse(surf, (22, 18, 12), (cx-22, cy-12, 44, 24))
            pygame.draw.ellipse(surf, (12, 10, 6),  (cx-16, cy-8,  32, 16))
            pygame.draw.ellipse(surf, (35, 28, 20), (cx-8,  cy-4,  10, 8))
        elif self.kind == 'barrier':
            for i in range(5):
                c = (255,55,55) if i % 2 == 0 else (255,255,255)
                pygame.draw.rect(surf, c, (cx - 26 + i*10, cy - 8, 10, 16))
            pygame.draw.rect(surf, (180,180,180), (cx-26, cy-8, 52, 16), 2, border_radius=2)


class PowerUp:
    def __init__(self, kind, road_speed):
        self.kind   = kind
        self.lane   = random.randint(0, LANE_COUNT - 1)
        self.x      = float(LANE_CX[self.lane])
        self.y      = float(-30)
        self.speed  = road_speed
        self.r      = 18
        self.life   = 320
        self.phase  = random.uniform(0, math.pi * 2)

    def update(self, road_speed):
        self.y    += road_speed
        self.life -= 1
        self.phase = (self.phase + 0.14) % (math.pi * 2)

    def rect(self):
        return pygame.Rect(int(self.x) - self.r, int(self.y) - self.r, self.r*2, self.r*2)

    def gone(self):
        return self.life <= 0 or self.y > H + self.r

    def draw(self, surf):
        _init_fonts()
        color = PU_COLOR[self.kind]
        pr = self.r + int(3 * math.sin(self.phase))
        pygame.draw.circle(surf, color,           (int(self.x), int(self.y)), pr)
        pygame.draw.circle(surf, (255,255,255),   (int(self.x), int(self.y)), pr, 2)
        label = {'nitro': 'N', 'shield': 'S', 'repair': 'R'}[self.kind]
        t = _F_PU.render(label, True, (255,255,255))
        surf.blit(t, t.get_rect(center=(int(self.x), int(self.y))))


class Coin:
    def __init__(self, road_speed):
        d = random.choices(COIN_POOL, weights=[p['w'] for p in COIN_POOL])[0]
        self.value = d['value']
        self.color = d['color']
        self.r     = d['r']
        self.lane  = random.randint(0, LANE_COUNT - 1)
        self.x     = float(LANE_CX[self.lane])
        self.y     = float(-30)
        self.speed = road_speed
        self.phase = random.uniform(0, math.pi * 2)

    def update(self, road_speed):
        self.y    += road_speed
        self.phase = (self.phase + 0.09) % (math.pi * 2)

    def rect(self):
        return pygame.Rect(int(self.x) - self.r, int(self.y) - self.r, self.r*2, self.r*2)

    def gone(self):
        return self.y > H + self.r

    def draw(self, surf):
        _init_fonts()
        pr = self.r + int(2 * math.sin(self.phase))
        pygame.draw.circle(surf, self.color,        (int(self.x), int(self.y)), pr)
        pygame.draw.circle(surf, (255,240,180),     (int(self.x), int(self.y)), pr, 2)
        if self.value > 1:
            t = _F_SM.render(str(self.value), True, (255,255,255))
            surf.blit(t, t.get_rect(center=(int(self.x), int(self.y))))


class Game:
    COURSE = 6000

    def __init__(self, username, settings):
        _init_fonts()
        self.username = username
        ds = DIFF.get(settings.get('difficulty', 'normal'), DIFF['normal'])
        cc = CAR_COLORS.get(settings.get('car_color', 'red'), CAR_COLORS['red'])

        self.base_speed  = ds['speed']
        self.road_speed  = ds['speed']
        self._t_int      = ds['traffic']
        self._o_int      = ds['obstacle']
        self._c_int      = ds['coin']

        self.road    = Road(self.road_speed)
        self.player  = Player(cc)

        self.traffic   = []
        self.obstacles = []
        self.powerups  = []
        self.coins     = []

        self.score          = 0
        self.coins_total    = 0
        self.distance       = 0.0
        self.frame          = 0

        self.active_pu  = None
        self.pu_timer   = 0

        self._tt  = self._t_int
        self._ot  = self._o_int
        self._ct  = self._c_int
        self._put = random.randint(220, 420)

        self.over      = False
        self.slow_warn = False

        self._fn     = pygame.font.SysFont('Arial', 17)
        self._fn_big = pygame.font.SysFont('Arial', 26, bold=True)
        self._fn_sm  = pygame.font.SysFont('Arial', 13)

    def _scale_speed(self):
        self.road_speed = min(self.base_speed + self.frame // 360 * 0.55, self.base_speed * 2.6)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and not self.over:
            if event.key == pygame.K_LEFT:
                self.player.move(-1)
            elif event.key == pygame.K_RIGHT:
                self.player.move(1)

    def update(self):
        if self.over:
            return
        self.frame    += 1
        self.distance += self.road_speed * 0.048
        self.score     = int(self.distance * 0.5) + self.coins_total * 10

        if self.frame % 300 == 0:
            self._scale_speed()

        eff = self.road_speed * self.player.smult
        self.slow_warn = self.road.in_slow(self.player.lane, self.player.y)
        in_nitro_strip = self.road.in_nitro(self.player.lane, self.player.y)

        if self.slow_warn and self.active_pu != 'nitro':
            self.road.speed = max(2.0, eff * 0.48)
        elif in_nitro_strip and self.active_pu != 'nitro':
            self.road.speed = eff * 1.55
        else:
            self.road.speed = eff

        self.road.update()
        self.player.update()

        self._tt -= 1
        if self._tt <= 0:
            self.traffic.append(TrafficCar(self.road_speed))
            self._tt = max(28, int(self._t_int - self.frame // 420))

        self._ot -= 1
        if self._ot <= 0:
            kind = random.choice(['oil', 'pothole', 'barrier'])
            self.obstacles.append(Obstacle(kind, self.road_speed))
            self._ot = max(38, int(self._o_int - self.frame // 320))

        self._ct -= 1
        if self._ct <= 0:
            self.coins.append(Coin(self.road_speed))
            self._ct = self._c_int

        self._put -= 1
        if self._put <= 0:
            kind = random.choice(['nitro', 'shield', 'repair'])
            self.powerups.append(PowerUp(kind, self.road_speed))
            self._put = random.randint(300, 620)

        rs = self.road_speed
        for e in self.traffic:   e.update(rs)
        for o in self.obstacles: o.update(rs)
        for p in self.powerups:  p.update(rs)
        for c in self.coins:     c.update(rs)

        if self.pu_timer > 0:
            self.pu_timer -= 1
            if self.pu_timer == 0:
                if self.active_pu == 'nitro':
                    self.player.smult   = 1.0
                    self.player.nitro_t = 0
                self.active_pu = None
        if self.active_pu == 'shield' and not self.player.shield:
            self.active_pu = None

        pr = self.player.rect()

        for t in self.traffic[:]:
            if t.rect().colliderect(pr):
                if self.player.shield:
                    self.player.shield  = False
                    self.player.s_flash = 40
                    self.traffic.remove(t)
                else:
                    self.over = True
                    return

        for o in self.obstacles[:]:
            if o.rect().colliderect(pr):
                if self.player.shield:
                    self.player.shield  = False
                    self.player.s_flash = 40
                    self.obstacles.remove(o)
                else:
                    self.over = True
                    return

        for c in self.coins[:]:
            if c.rect().colliderect(pr):
                self.coins_total += c.value
                self.score       += c.value * 10
                self.road_speed   = min(self.road_speed + 0.06, self.base_speed * 3.0)
                self.coins.remove(c)

        for p in self.powerups[:]:
            if p.rect().colliderect(pr):
                self._apply_pu(p.kind)
                self.powerups.remove(p)

        self.traffic   = [t for t in self.traffic   if not t.gone()]
        self.obstacles = [o for o in self.obstacles if not o.gone()]
        self.powerups  = [p for p in self.powerups  if not p.gone()]
        self.coins     = [c for c in self.coins     if not c.gone()]

    def _apply_pu(self, kind):
        self.active_pu = kind
        if kind == 'nitro':
            self.player.smult   = 1.85
            self.player.nitro_t = 240
            self.pu_timer       = 240
            self.score         += 50
        elif kind == 'shield':
            self.player.shield = True
            self.pu_timer      = 0
        elif kind == 'repair':
            if self.obstacles:
                self.obstacles.pop(0)
            self.score    += 30
            self.pu_timer = 110

    def draw(self, surf):
        self.road.draw(surf)
        for c in self.coins:     c.draw(surf)
        for p in self.powerups:  p.draw(surf)
        for o in self.obstacles: o.draw(surf)
        for t in self.traffic:   t.draw(surf)
        self.player.draw(surf)
        self._draw_hud(surf)

    def _draw_hud(self, surf):
        pygame.draw.rect(surf, (30, 30, 40), (0, 0, W, 56))
        pygame.draw.line(surf, (60, 60, 80), (0, 56), (W, 56), 2)

        draw_text(surf, f'Score: {self.score}',        (10, 8),  self._fn,    (255,255,255))
        draw_text(surf, f'Coins: {self.coins_total}',  (10, 30), self._fn,    (255,210,0))
        draw_text(surf, f'Speed: {int(self.road_speed*18)}', (170, 8),  self._fn, (200,200,200))

        dist  = int(self.distance)
        remain = max(0, self.COURSE - dist)
        draw_text(surf, f'{dist}m  /{remain}m left', (170, 30), self._fn, (160,210,255))

        if self.active_pu:
            color = PU_COLOR.get(self.active_pu, (255,255,255))
            label = self.active_pu.upper()
            if self.active_pu == 'nitro' and self.pu_timer > 0:
                label += f' {self.pu_timer//60}s'
            t = self._fn_big.render(label, True, color)
            surf.blit(t, t.get_rect(midright=(W - 10, 28)))

        if self.slow_warn:
            t = self._fn_sm.render('SLOW ZONE', True, (255,130,0))
            surf.blit(t, t.get_rect(center=(W//2, H - 28)))

        if self.player.shield:
            t = self._fn_sm.render('SHIELD', True, (80,180,255))
            surf.blit(t, t.get_rect(midright=(W - 10, H - 28)))


def draw_text(surf, text, pos, font, color=(255,255,255)):
    s = font.render(text, True, color)
    surf.blit(s, pos)