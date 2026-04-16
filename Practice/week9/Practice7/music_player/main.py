import pygame
from player import MusicPlayer

# --- Constants ---
SCREEN_WIDTH  = 620
SCREEN_HEIGHT = 420
FPS           = 30
BG_COLOR      = (28, 28, 35)
COLOR_ACCENT  = (72, 199, 142)   # green
COLOR_WHITE   = (230, 230, 230)
COLOR_GRAY    = (140, 140, 150)
COLOR_DIM     = (60, 60, 70)


def draw_ui(screen, fonts, player: MusicPlayer):
    """Draw all text elements: title, track name, status, instructions."""
    font_title, font_track, font_info = fonts
    cx = SCREEN_WIDTH // 2

    # --- Title ---
    title = font_title.render("🎵  Music Player", True, COLOR_ACCENT)
    screen.blit(title, (cx - title.get_width() // 2, 30))

    # --- Divider line ---
    pygame.draw.line(screen, COLOR_DIM, (40, 80), (SCREEN_WIDTH - 40, 80), 1)

    # --- Current track ---
    label = font_info.render("NOW PLAYING", True, COLOR_GRAY)
    screen.blit(label, (cx - label.get_width() // 2, 100))

    track = font_track.render(player.get_track_name(), True, COLOR_WHITE)
    screen.blit(track, (cx - track.get_width() // 2, 130))

    # --- Status ---
    status = font_info.render(player.get_status(), True, COLOR_ACCENT)
    screen.blit(status, (cx - status.get_width() // 2, 180))

    # --- Divider line ---
    pygame.draw.line(screen, COLOR_DIM, (40, 220), (SCREEN_WIDTH - 40, 220), 1)

    # --- Controls ---
    controls = [
        ("[P]  Play",          COLOR_WHITE),
        ("[S]  Stop",          COLOR_WHITE),
        ("[N]  Next Track",    COLOR_WHITE),
        ("[B]  Previous Track",COLOR_WHITE),
        ("[Q]  Quit",          COLOR_GRAY),
    ]
    for i, (text, color) in enumerate(controls):
        surf = font_info.render(text, True, color)
        screen.blit(surf, (cx - surf.get_width() // 2, 240 + i * 32))


def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Music Player")
    clock = pygame.time.Clock()

    # Fonts
    fonts = (
        pygame.font.SysFont("Arial", 30, bold=True),   # title
        pygame.font.SysFont("Arial", 22),               # track name
        pygame.font.SysFont("Arial", 19),               # info / controls
    )

    player = MusicPlayer(music_folder="music")

    running = True
    while running:

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    player.play()
                elif event.key == pygame.K_s:
                    player.stop()
                elif event.key == pygame.K_n:
                    player.next_track()
                elif event.key == pygame.K_b:
                    player.prev_track()
                elif event.key == pygame.K_q:
                    running = False

        # --- Draw ---
        screen.fill(BG_COLOR)
        draw_ui(screen, fonts, player)
        pygame.display.flip()
        clock.tick(FPS)

    player.stop()
    pygame.quit()


if __name__ == "__main__":
    main()