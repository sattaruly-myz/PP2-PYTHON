import pygame
import sys
import json
import os

from config import WINDOW_W, WINDOW_H, HUD_H, GRID, COLS, ROWS, FPS, BASE_SPEED, FOOD_PER_LEVEL
from game import Game, PU_COLORS, PU_SPEED, PU_SLOW, PU_SHIELD
import db

SETTINGS_FILE = "settings.json"
DEFAULT_SETTINGS = {"snake_color": [0, 180, 0], "grid": False, "sound": False}

S_MENU = "menu"
S_PLAY = "play"
S_OVER = "over"
S_LEADERBOARD = "leaderboard"
S_SETTINGS = "settings"

COLOR_SWATCHES = [
    [0, 180, 0],
    [0, 120, 255],
    [255, 100, 0],
    [200, 0, 200],
    [0, 200, 200],
    [255, 200, 0],
]


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return DEFAULT_SETTINGS.copy()


def save_settings_file(s):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(s, f, indent=2)


def font(size):
    return pygame.font.SysFont("Arial", size, bold=False)


def draw_text(surf, text, size, color, x, y, anchor="center"):
    img = font(size).render(text, True, color)
    r = img.get_rect()
    setattr(r, anchor, (x, y))
    surf.blit(img, r)
    return r


def btn(surf, text, x, y, w, h, mouse, base_color=(55, 55, 175)):
    r = pygame.Rect(x, y, w, h)
    c = tuple(min(v + 35, 255) for v in base_color) if r.collidepoint(mouse) else base_color
    pygame.draw.rect(surf, c, r, border_radius=8)
    pygame.draw.rect(surf, (180, 180, 180), r, 2, border_radius=8)
    draw_text(surf, text, 21, (255, 255, 255), x + w // 2, y + h // 2)
    return r


def clicked(events, rect):
    for e in events:
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and rect.collidepoint(e.pos):
            return True
    return False


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    try:
        db.init_db()
        db_ok = True
    except Exception:
        db_ok = False

    settings = load_settings()
    state = S_MENU

    username = ""
    entering_name = True
    player_id = None
    personal_best = 0

    game = None
    game_timer = 0
    game_saved = False

    leaderboard_data = []
    swatch_idx = 0

    def start_game():
        nonlocal game, game_timer, player_id, personal_best, game_saved
        sc = tuple(settings["snake_color"])
        game = Game(COLS, ROWS, BASE_SPEED, FOOD_PER_LEVEL, sc)
        game_timer = 0
        game_saved = False
        if db_ok and username.strip():
            try:
                player_id = db.get_or_create_player(username.strip())
                personal_best = db.get_personal_best(player_id)
            except Exception:
                player_id = None
                personal_best = 0

    def save_result():
        nonlocal personal_best, game_saved
        if game_saved:
            return
        game_saved = True
        if db_ok and player_id is not None and game is not None:
            try:
                db.save_session(player_id, game.score, game.level)
                personal_best = db.get_personal_best(player_id)
            except Exception:
                pass

    game_surf = pygame.Surface((WINDOW_W, WINDOW_H - HUD_H))

    while True:
        mouse = pygame.mouse.get_pos()
        events = pygame.event.get()

        for e in events:
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((14, 14, 24))

        if state == S_MENU:
            draw_text(screen, "SNAKE", 76, (0, 220, 80), WINDOW_W // 2, 75)

            if entering_name:
                draw_text(screen, "Enter username:", 24, (180, 180, 180), WINDOW_W // 2, 165)
                box = pygame.Rect(WINDOW_W // 2 - 150, 185, 300, 42)
                pygame.draw.rect(screen, (35, 35, 55), box, border_radius=7)
                pygame.draw.rect(screen, (80, 200, 100), box, 2, border_radius=7)
                draw_text(screen, username + "|", 24, (255, 255, 255), WINDOW_W // 2, box.centery)

                for e in events:
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_RETURN and username.strip():
                            entering_name = False
                        elif e.key == pygame.K_BACKSPACE:
                            username = username[:-1]
                        elif len(username) < 20 and e.unicode.isprintable() and e.unicode != "":
                            username += e.unicode
            else:
                draw_text(screen, f"Welcome, {username}!", 24, (100, 220, 100), WINDOW_W // 2, 185)

            bx, by, bw, bh = WINDOW_W // 2 - 105, 248, 210, 46
            play_r  = btn(screen, "Play",        bx, by,       bw, bh, mouse)
            lb_r    = btn(screen, "Leaderboard", bx, by + 60,  bw, bh, mouse)
            set_r   = btn(screen, "Settings",    bx, by + 120, bw, bh, mouse)
            quit_r  = btn(screen, "Quit",        bx, by + 180, bw, bh, mouse, (130, 35, 35))

            if not entering_name and clicked(events, play_r):
                start_game()
                state = S_PLAY
            if clicked(events, lb_r):
                leaderboard_data = db.get_leaderboard() if db_ok else []
                state = S_LEADERBOARD
            if clicked(events, set_r):
                try:
                    swatch_idx = COLOR_SWATCHES.index(settings["snake_color"])
                except ValueError:
                    swatch_idx = 0
                state = S_SETTINGS
            if clicked(events, quit_r):
                pygame.quit()
                sys.exit()

        elif state == S_PLAY:
            for e in events:
                if e.type == pygame.KEYDOWN:
                    if e.key in (pygame.K_UP,    pygame.K_w): game.set_dir((0, -1))
                    elif e.key in (pygame.K_DOWN,  pygame.K_s): game.set_dir((0, 1))
                    elif e.key in (pygame.K_LEFT,  pygame.K_a): game.set_dir((-1, 0))
                    elif e.key in (pygame.K_RIGHT, pygame.K_d): game.set_dir((1, 0))
                    elif e.key == pygame.K_ESCAPE:
                        state = S_MENU

            dt = clock.get_time()
            game_timer += dt
            step_ms = max(50, 1000 // game.speed)
            while game_timer >= step_ms:
                game_timer -= step_ms
                game.update()

            game_surf.fill((14, 14, 24))
            game.draw(game_surf, settings["grid"], GRID)
            screen.blit(game_surf, (0, HUD_H))

            pygame.draw.rect(screen, (20, 20, 35), (0, 0, WINDOW_W, HUD_H))
            pygame.draw.line(screen, (50, 50, 80), (0, HUD_H), (WINDOW_W, HUD_H), 1)

            hf = font(20)
            hud_items = [
                f"Score: {game.score}",
                f"Level: {game.level}",
                f"Best: {personal_best}",
            ]
            if game.shield:
                hud_items.append("SHIELD ✦")
            if game.effect:
                left = max(0, (game.effect_end - pygame.time.get_ticks()) // 1000)
                label = {"speed": "SPEED", "slow": "SLOW"}[game.effect]
                hud_items.append(f"{label} {left}s")

            for i, t in enumerate(hud_items):
                img = hf.render(t, True, (210, 210, 210))
                screen.blit(img, (10 + i * 170, (HUD_H - img.get_height()) // 2))

            if game.over:
                save_result()
                state = S_OVER

        elif state == S_OVER:
            draw_text(screen, "GAME OVER", 68, (220, 45, 45), WINDOW_W // 2, 140)
            draw_text(screen, f"Score: {game.score}", 38, (255, 255, 255), WINDOW_W // 2, 255)
            draw_text(screen, f"Level reached: {game.level}", 30, (180, 180, 180), WINDOW_W // 2, 310)
            draw_text(screen, f"Personal Best: {personal_best}", 28, (255, 215, 0), WINDOW_W // 2, 358)

            cx = WINDOW_W // 2
            retry_r = btn(screen, "Retry",     cx - 130, 420, 110, 46, mouse)
            menu_r  = btn(screen, "Main Menu", cx + 20,  420, 130, 46, mouse)

            if clicked(events, retry_r):
                start_game()
                state = S_PLAY
            if clicked(events, menu_r):
                entering_name = False
                state = S_MENU

        elif state == S_LEADERBOARD:
            draw_text(screen, "LEADERBOARD", 50, (0, 220, 80), WINDOW_W // 2, 48)

            col_x = [40, 110, 360, 460, 570]
            headers = ["#", "Username", "Score", "Level", "Date"]
            hy = 105
            for i, h in enumerate(headers):
                draw_text(screen, h, 20, (120, 180, 255), col_x[i], hy, anchor="topleft")
            pygame.draw.line(screen, (70, 70, 110), (30, 130), (WINDOW_W - 30, 130), 1)

            for rank, row in enumerate(leaderboard_data, 1):
                ry = 136 + (rank - 1) * 36
                color = (255, 215, 0) if rank == 1 else (200, 200, 200)
                vals = [str(rank), str(row[0]), str(row[1]), str(row[2]), str(row[3])]
                for i, v in enumerate(vals):
                    draw_text(screen, v, 19, color, col_x[i], ry, anchor="topleft")

            back_r = btn(screen, "Back", WINDOW_W // 2 - 65, 560, 130, 42, mouse)
            if clicked(events, back_r):
                state = S_MENU

        elif state == S_SETTINGS:
            draw_text(screen, "SETTINGS", 50, (0, 220, 80), WINDOW_W // 2, 55)

            draw_text(screen, "Snake Color", 26, (180, 180, 180), WINDOW_W // 2, 140)
            sw, sg = 44, 12
            total = len(COLOR_SWATCHES) * sw + (len(COLOR_SWATCHES) - 1) * sg
            sx0 = WINDOW_W // 2 - total // 2
            for i, col in enumerate(COLOR_SWATCHES):
                sx = sx0 + i * (sw + sg)
                pygame.draw.rect(screen, col, (sx, 165, sw, sw), border_radius=7)
                if i == swatch_idx:
                    pygame.draw.rect(screen, (255, 255, 255), (sx - 3, 162, sw + 6, sw + 6), 3, border_radius=7)
                for e in events:
                    if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                        if pygame.Rect(sx, 165, sw, sw).collidepoint(e.pos):
                            swatch_idx = i

            grid_col = (35, 105, 35) if settings["grid"] else (90, 35, 35)
            grid_r = btn(screen, f"Grid: {'ON' if settings['grid'] else 'OFF'}",
                         WINDOW_W // 2 - 90, 250, 180, 46, mouse, grid_col)

            snd_col = (35, 105, 35) if settings["sound"] else (90, 35, 35)
            snd_r = btn(screen, f"Sound: {'ON' if settings['sound'] else 'OFF'}",
                        WINDOW_W // 2 - 90, 318, 180, 46, mouse, snd_col)

            save_r = btn(screen, "Save & Back", WINDOW_W // 2 - 90, 400, 180, 46, mouse)

            if clicked(events, grid_r):
                settings["grid"] = not settings["grid"]
            if clicked(events, snd_r):
                settings["sound"] = not settings["sound"]
            if clicked(events, save_r):
                settings["snake_color"] = COLOR_SWATCHES[swatch_idx]
                save_settings_file(settings)
                state = S_MENU

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()