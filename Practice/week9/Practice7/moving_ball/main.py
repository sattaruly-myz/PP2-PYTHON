import pygame
from ball import Ball

# --- Constants ---
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
FPS           = 60
STEP          = 20          # pixels per key press
BG_COLOR      = (255, 255, 255)
BALL_RADIUS   = 25


def draw_instructions(screen: pygame.Surface, font: pygame.font.Font):
    """Render control instructions in the top-left corner."""
    lines = [
        "Arrow Keys — Move Ball",
        "ESC — Quit",
    ]
    for i, line in enumerate(lines):
        text = font.render(line, True, (100, 100, 100))
        screen.blit(text, (10, 10 + i * 22))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Moving Ball Game")
    clock  = pygame.time.Clock()
    font   = pygame.font.SysFont("Arial", 18)

    # Create ball in the center of the screen
    ball = Ball(
        x=SCREEN_WIDTH  // 2,
        y=SCREEN_HEIGHT // 2,
        radius=BALL_RADIUS,
        screen_width=SCREEN_WIDTH,
        screen_height=SCREEN_HEIGHT,
    )

    running = True
    while running:

        # --- Event handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_LEFT:
                    ball.move(-STEP, 0)
                elif event.key == pygame.K_RIGHT:
                    ball.move(STEP, 0)
                elif event.key == pygame.K_UP:
                    ball.move(0, -STEP)
                elif event.key == pygame.K_DOWN:
                    ball.move(0, STEP)

        # --- Drawing ---
        screen.fill(BG_COLOR)
        draw_instructions(screen, font)
        ball.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()