import pygame
import sys
from ui import Button, TextInput, draw_text
from racer import Game, W, H, CAR_COLORS
from persistence import load_settings, save_settings, load_leaderboard, add_score

pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('Racer')
clock = pygame.time.Clock()

FN     = pygame.font.SysFont('Arial', 20)
FN_BIG = pygame.font.SysFont('Arial', 34, bold=True)
FN_TTL = pygame.font.SysFont('Arial', 58, bold=True)
FN_SM  = pygame.font.SysFont('Arial', 16)
FN_LB  = pygame.font.SysFont('Courier', 17)

BG1 = (12, 12, 22)
BG2 = (18, 18, 30)

# STATE управляет тем, какой экран сейчас видит пользователь
STATE    = 'menu'
settings = load_settings()
username = ''
game     = None
results  = None

CX = W // 2 # выравнивание чтобы было удобно

menu_btns = [
    Button((CX-110, 230, 220, 52), 'Play',        FN_BIG),
    Button((CX-110, 298, 220, 52), 'Leaderboard', FN_BIG),
    Button((CX-110, 366, 220, 52), 'Settings',    FN_BIG),
    Button((CX-110, 434, 220, 52), 'Quit',        FN_BIG, color=(140,40,40), hover=(180,60,60)),
]

name_input = TextInput((CX-130, 340, 260, 46), FN_BIG, placeholder='Your name...')
name_btn   = Button((CX-110, 408, 220, 50), 'Play', FN_BIG)

DIFF_KEYS  = ('easy', 'normal', 'hard')
COLOR_KEYS = ('red', 'blue', 'green', 'yellow')
COLOR_VALS = [(195,45,45),(45,90,210),(45,175,70),(205,190,25)]

def snd_btn():
    lbl = 'Sound: ON' if settings['sound'] else 'Sound: OFF'
    c   = (40,140,60) if settings['sound'] else (100,100,100)
    return Button((CX-110, 215, 220, 46), lbl, FN, color=c, hover=c)

def diff_btns():
    return [Button((CX-170+i*115, 310, 105, 44), k.capitalize(), FN,
                   color=(40,130,60) if settings['difficulty']==k else (60,110,185))
            for i,k in enumerate(DIFF_KEYS)]

def color_btns():
    return [Button((CX-185+i*92, 420, 84, 44), k.capitalize(), FN,
                   color=COLOR_VALS[i], hover=tuple(min(255,v+30) for v in COLOR_VALS[i]))
            for i,k in enumerate(COLOR_KEYS)]

s_back  = Button((CX-110, 510, 220, 46), 'Back', FN)
lb_back = Button((CX-110, H-80, 220, 46), 'Back', FN)
go_retry = Button((CX-115, 510, 220, 52), 'Retry',     FN_BIG)
go_menu  = Button((CX-115, 578, 220, 52), 'Main Menu', FN_BIG)


def draw_bg(surf): # фон
    surf.fill(BG1)
    for gy in range(0, H, 75):
        for gx in range(0, W, 75):
            pygame.draw.rect(surf, BG2, (gx+1, gy+1, 73, 73))


def screen_menu(surf):
    draw_bg(surf)
    t = FN_TTL.render('RACER', True, (70,140,215))
    surf.blit(t, t.get_rect(center=(CX, 138)))
    sub = FN_SM.render('Arcade Road Runner', True, (90,90,120))
    surf.blit(sub, sub.get_rect(center=(CX, 192)))
    for b in menu_btns:
        b.draw(surf)


def screen_name(surf):
    draw_bg(surf)
    t = FN_BIG.render('Enter Your Name', True, (255,255,255))
    surf.blit(t, t.get_rect(center=(CX, 265)))
    name_input.draw(surf)
    name_btn.draw(surf)


def screen_settings(surf): # сложность и цвет машын
    draw_bg(surf)
    t = FN_BIG.render('Settings', True, (255,255,255))
    surf.blit(t, t.get_rect(center=(CX, 140)))

    draw_text(surf, 'Sound', (CX, 192), FN_SM, (160,160,160), center=True)
    snd_btn().draw(surf)

    draw_text(surf, 'Difficulty', (CX, 288), FN_SM, (160,160,160), center=True)
    for b in diff_btns():
        b.draw(surf)

    draw_text(surf, 'Car Color', (CX, 398), FN_SM, (160,160,160), center=True)
    for i, b in enumerate(color_btns()):
        b.draw(surf)
        if settings['car_color'] == COLOR_KEYS[i]:
            pygame.draw.rect(surf, (255,255,255), b.rect, 3, border_radius=8)

    s_back.draw(surf)


def screen_leaderboard(surf):
    draw_bg(surf)
    t = FN_BIG.render('Leaderboard', True, (255,210,0))
    surf.blit(t, t.get_rect(center=(CX, 80)))

    hdr = FN_LB.render(f"{'#':<3}  {'Name':<16}  {'Score':>7}  {'Dist':>7}", True, (140,140,160))
    surf.blit(hdr, (55, 130))
    pygame.draw.line(surf, (55,55,75), (55,153), (W-55,153), 1)

    lb = load_leaderboard()
    for i, e in enumerate(lb[:10]):
        y   = 162 + i * 36
        col = (255,210,0) if i==0 else (200,200,200) if i<3 else (140,140,140)
        row = f"{i+1:<3}  {e['name']:<16}  {e['score']:>7}  {e['distance']:>6}m"
        surf.blit(FN_LB.render(row, True, col), (55, y))

    if not lb:
        t = FN.render('No scores yet!', True, (90,90,110))
        surf.blit(t, t.get_rect(center=(CX, 320)))

    lb_back.draw(surf)


def screen_gameover(surf, res):
    draw_bg(surf)
    t = FN_TTL.render('GAME OVER', True, (215,45,45))
    surf.blit(t, t.get_rect(center=(CX, 130)))

    items = [
        (f"Score:    {res['score']}",    (255,255,255)),
        (f"Distance: {res['distance']}m",(165,210,255)),
        (f"Coins:    {res['coins']}",    (255,210,0)),
    ]
    for i,(txt,col) in enumerate(items):
        t = FN_BIG.render(txt, True, col)
        surf.blit(t, t.get_rect(center=(CX, 258 + i*62)))

    go_retry.draw(surf)
    go_menu.draw(surf)


def draw_text(surf, text, pos, font, color=(255,255,255), center=False):
    s = font.render(text, True, color)
    r = s.get_rect(center=pos) if center else s.get_rect(topleft=pos)
    surf.blit(s, r)


running = True
while running:
    click = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click = event.pos

        if STATE == 'menu':
            if click:
                if menu_btns[0].clicked(click): STATE = 'name'
                elif menu_btns[1].clicked(click): STATE = 'leaderboard'
                elif menu_btns[2].clicked(click): STATE = 'settings'
                elif menu_btns[3].clicked(click): running = False

        elif STATE == 'name':
            done = name_input.handle(event)
            if click and name_btn.clicked(click):
                done = True
            if done and name_input.text.strip():
                username = name_input.text.strip()
                game = Game(username, settings)
                STATE = 'playing'

        elif STATE == 'settings':
            if click:
                sb = snd_btn()
                if sb.clicked(click):
                    settings['sound'] = not settings['sound']
                    save_settings(settings)
                for i, b in enumerate(diff_btns()):
                    if b.clicked(click):
                        settings['difficulty'] = DIFF_KEYS[i]
                        save_settings(settings)
                for i, b in enumerate(color_btns()):
                    if b.clicked(click):
                        settings['car_color'] = COLOR_KEYS[i]
                        save_settings(settings)
                if s_back.clicked(click):
                    STATE = 'menu'

        elif STATE == 'leaderboard':
            if click and lb_back.clicked(click):
                STATE = 'menu'

        elif STATE == 'playing':
            if game:
                game.handle_event(event)

        elif STATE == 'gameover':
            if click:
                if go_retry.clicked(click):
                    game  = Game(username, settings)
                    STATE = 'playing'
                elif go_menu.clicked(click):
                    STATE = 'menu'

    if STATE == 'playing' and game:
        game.update()
        if game.over:
            results = game.get_results()
            add_score(username, results['score'], results['distance'])
            STATE = 'gameover'

    if   STATE == 'menu':        screen_menu(screen)
    elif STATE == 'name':        screen_name(screen)
    elif STATE == 'settings':    screen_settings(screen)
    elif STATE == 'leaderboard': screen_leaderboard(screen)
    elif STATE == 'playing' and game:
        screen.fill(BG1)
        game.draw(screen)
    elif STATE == 'gameover' and results:
        screen_gameover(screen, results)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()