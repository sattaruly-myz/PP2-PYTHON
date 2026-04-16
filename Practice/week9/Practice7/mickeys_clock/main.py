import pygame
from clock import Clock

# --- Constants ---
SCREEN_WIDTH  = 600
SCREEN_HEIGHT = 600
FPS           = 1           # update once per second is enough for a clock
BG_COLOR      = (245, 235, 215)


def draw_time_text(screen: pygame.Surface, font: pygame.font.Font):
    """Show the current digital time below the clock face."""
    import datetime
    now = datetime.datetime.now()
    time_str = now.strftime("%H:%M:%S")
    text = font.render(time_str, True, (60, 60, 60))
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT - 60))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Mickey's Clock")
    ticker = pygame.time.Clock()
    font   = pygame.font.SysFont("Arial", 28, bold=True)

    # Create the clock object (center of screen is used inside the class)
    mickey_clock = Clock(SCREEN_WIDTH, SCREEN_HEIGHT)

    running = True
    while running:

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # --- Draw ---
        screen.fill(BG_COLOR)
        mickey_clock.draw(screen)       # draw clock face + both hands
        draw_time_text(screen, font)    # draw digital time at the bottom
        pygame.display.flip()
        ticker.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()