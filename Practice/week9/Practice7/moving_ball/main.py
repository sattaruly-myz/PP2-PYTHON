import pygame
import sys
from ball import Ball, WIDTH, HEIGHT


pygame.init()

SCREEN_WIDTH = WIDTH
SCREEN_HEIGHT = HEIGHT
WHITE = (255, 255, 255)
MOVE_STEP = 20
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Moving Ball Game")

ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ball.move(0, -MOVE_STEP)
            elif event.key == pygame.K_DOWN:
                ball.move(0, MOVE_STEP)
            elif event.key == pygame.K_LEFT:
                ball.move(-MOVE_STEP, 0)
            elif event.key == pygame.K_RIGHT:
                ball.move(MOVE_STEP, 0)

    screen.fill(WHITE)
    ball.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()