from __future__ import annotations

import pygame


WIDTH, HEIGHT = 640, 480
BALL_RADIUS = 25


class Ball:
    def __init__(self, x: int, y: int, radius: int = BALL_RADIUS):
        self.x = x
        self.y = y
        self.radius = radius

    def move(self, dx: int, dy: int) -> None:
        new_x = self.x + dx
        new_y = self.y + dy

        if new_x - self.radius < 0 or new_x + self.radius > WIDTH:
            new_x = self.x
        if new_y - self.radius < 0 or new_y + self.radius > HEIGHT:
            new_y = self.y

        self.x = new_x
        self.y = new_y

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)