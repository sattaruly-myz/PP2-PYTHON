from __future__ import annotations

import random
import pygame


WIDTH, HEIGHT = 640, 480
BALL_RADIUS = 25


class Ball:
    def __init__(self, x: int, y: int, radius: int = BALL_RADIUS):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = self.random_color()

    def random_color(self) -> tuple[int, int, int]:
        return (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )

    def move(self, dx: int, dy: int) -> None:
        new_x = self.x + dx
        new_y = self.y + dy
        hit_wall = False

        if new_x - self.radius < 0:
            new_x = self.radius
            hit_wall = True
        elif new_x + self.radius > WIDTH:
            new_x = WIDTH - self.radius
            hit_wall = True

        if new_y - self.radius < 0:
            new_y = self.radius
            hit_wall = True
        elif new_y + self.radius > HEIGHT:
            new_y = HEIGHT - self.radius
            hit_wall = True

        self.x = new_x
        self.y = new_y

        if hit_wall:
            self.color = self.random_color()

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)