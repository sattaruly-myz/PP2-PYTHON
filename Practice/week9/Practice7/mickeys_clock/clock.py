import pygame
import datetime
import math


class Clock:
    """
    Mickey Mouse clock.
    - Right hand (screen-right) = minute hand
    - Left  hand (screen-left)  = second hand

    Expects 'images/mickey_hand.png' to be a hand pointing UPWARD (12 o'clock).
    Uses pygame.transform.rotate() to spin it to the correct angle.
    """

    HAND_OFFSET = 70    # horizontal distance from center to each hand pivot
    FACE_RADIUS = 160   # radius of the clock face circle

    def __init__(self, screen_width: int, screen_height: int):
        self.cx = screen_width  // 2
        self.cy = screen_height // 2

        # Load the hand image (pointing up = 12 o'clock position)
        try:
            raw = pygame.image.load("images/mickey_hand.png").convert_alpha()
            # Scale to a reasonable size if needed
            self.hand_img = pygame.transform.scale(raw, (40, 100))
        except FileNotFoundError:
            # Fallback: draw a simple white rounded rectangle as the hand
            self.hand_img = self._make_fallback_hand(40, 100)

    # ------------------------------------------------------------------ #
    #  Private helpers                                                     #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _make_fallback_hand(w: int, h: int) -> pygame.Surface:
        """Create a simple hand shape when the image file is missing."""
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 255, 255), (6, 0, w - 12, h), border_radius=8)
        pygame.draw.circle(surf, (255, 220, 180), (w // 2, h - 12), 14)  # glove tip
        return surf

    def _angle_for_seconds(self, second: int) -> float:
        """Convert seconds (0-59) to clock angle in degrees (0 = 12 o'clock, CW)."""
        return (second / 60.0) * 360.0

    def _angle_for_minutes(self, minute: int, second: int) -> float:
        """Convert minutes + seconds to a smooth clock angle."""
        return ((minute + second / 60.0) / 60.0) * 360.0

    def _draw_hand(self, surface: pygame.Surface, angle_deg: float, offset_x: int):
        """
        Rotate the hand image by angle_deg (clockwise from 12 o'clock)
        and blit it at (cx + offset_x, cy).

        pygame.transform.rotate() goes counter-clockwise, so we negate.
        """
        rotated = pygame.transform.rotate(self.hand_img, -angle_deg)
        rect = rotated.get_rect(center=(self.cx + offset_x, self.cy))
        surface.blit(rotated, rect)

    def _draw_face(self, surface: pygame.Surface):
        """Draw a simple circular clock face with hour markers."""
        # Main circle
        pygame.draw.circle(surface, (255, 245, 220), (self.cx, self.cy), self.FACE_RADIUS)
        pygame.draw.circle(surface, (30, 30, 30),   (self.cx, self.cy), self.FACE_RADIUS, 3)

        # Hour markers (12 dots around the circle)
        for i in range(12):
            angle_rad = math.radians(i * 30 - 90)  # start at 12 o'clock
            r = self.FACE_RADIUS - 18
            mx = int(self.cx + r * math.cos(angle_rad))
            my = int(self.cy + r * math.sin(angle_rad))
            dot_size = 6 if i % 3 == 0 else 3
            pygame.draw.circle(surface, (50, 50, 50), (mx, my), dot_size)

        # Center dot
        pygame.draw.circle(surface, (30, 30, 30), (self.cx, self.cy), 8)

    # ------------------------------------------------------------------ #
    #  Public                                                              #
    # ------------------------------------------------------------------ #

    def draw(self, surface: pygame.Surface):
        """Read current time, compute angles, and draw the clock."""
        now = datetime.datetime.now()

        minute_angle = self._angle_for_minutes(now.minute, now.second)
        second_angle = self._angle_for_seconds(now.second)

        self._draw_face(surface)

        # Right hand = minutes
        self._draw_hand(surface, minute_angle, offset_x=+self.HAND_OFFSET)
        # Left hand  = seconds
        self._draw_hand(surface, second_angle, offset_x=-self.HAND_OFFSET)