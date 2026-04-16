import pygame


class Ball:
    """
    Represents a red ball that moves around the screen.
    Handles movement and boundary checking internally.
    """

    def __init__(self, x: int, y: int, radius: int, screen_width: int, screen_height: int):
        self.x = x
        self.y = y
        self.radius = radius
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.color = (220, 50, 50)  # Red

    def move(self, dx: int, dy: int):
        """
        Move the ball by (dx, dy) pixels.
        After moving, clamp position so the ball stays inside the screen.
        """
        self.x += dx
        self.y += dy

        # --- Boundary checking ---
        # Left / Right walls
        if self.x - self.radius < 0:
            self.x = self.radius
        if self.x + self.radius > self.screen_width:
            self.x = self.screen_width - self.radius

        # Top / Bottom walls
        if self.y - self.radius < 0:
            self.y = self.radius
        if self.y + self.radius > self.screen_height:
            self.y = self.screen_height - self.radius

    def draw(self, surface: pygame.Surface):
        """Draw the ball as a filled circle with a dark border."""
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(surface, (150, 20, 20), (self.x, self.y), self.radius, 2)  # border