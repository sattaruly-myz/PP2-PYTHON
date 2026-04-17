import math
from pathlib import Path
import datetime as dt
import pygame


BASE_DIR = Path(__file__).resolve().parent
ASSET_PATH = BASE_DIR / "images" / "mickey_hand.png"


def load_hand_image() -> pygame.Surface:
    """Load the hand image and create a visible fallback if needed."""
    if ASSET_PATH.exists():
        return pygame.image.load(str(ASSET_PATH)).convert_alpha()

    # Fallback: simple hand-like surface if the image is missing
    surface = pygame.Surface((220, 80), pygame.SRCALPHA)
    pygame.draw.rect(surface, (180, 30, 30), (0, 20, 140, 40), border_radius=12)
    pygame.draw.rect(surface, (255, 225, 190), (120, 12, 85, 56), border_radius=18)
    pygame.draw.polygon(surface, (255, 225, 190), [(160, 10), (180, 2), (200, 12), (180, 22)])
    pygame.draw.circle(surface, (255, 225, 190), (198, 40), 10)
    return surface


def rotate_hand(image: pygame.Surface, angle_deg: float) -> pygame.Surface:
    """Rotate clockwise from the '12 o'clock' position.

    Pygame rotates counterclockwise for positive angles, so we invert the sign.
    """
    return pygame.transform.rotate(image, -angle_deg)


def time_to_angles(now: dt.datetime) -> tuple[float, float]:
    """Return (minute_angle, second_angle) where 0Â° points up and angles grow clockwise."""
    seconds = now.second + now.microsecond / 1_000_000
    minutes = now.minute + seconds / 60.0

    # 60 seconds -> 360 degrees and 60 minutes -> 360 degrees
    second_angle = seconds * 6.0
    minute_angle = minutes * 6.0
    return minute_angle, second_angle


def blit_center_rotated(screen: pygame.Surface, image: pygame.Surface, center: tuple[int, int]) -> None:
    rect = image.get_rect(center=center)
    screen.blit(image, rect)


def draw_clock_face(screen: pygame.Surface, center: tuple[int, int], radius: int) -> None:
    pygame.draw.circle(screen, (250, 250, 250), center, radius)
    pygame.draw.circle(screen, (40, 40, 40), center, radius, 4)

    # Hour marks for visual clarity
    for i in range(12):
        angle = math.radians(i * 30 - 90)
        inner = radius - 12
        outer = radius - 2
        x1 = center[0] + int(math.cos(angle) * inner)
        y1 = center[1] + int(math.sin(angle) * inner)
        x2 = center[0] + int(math.cos(angle) * outer)
        y2 = center[1] + int(math.sin(angle) * outer)
        pygame.draw.line(screen, (60, 60, 60), (x1, y1), (x2, y2), 3)


def main() -> None:
    pygame.init()
    pygame.display.set_caption("Mickey's Clock")
    screen = pygame.display.set_mode((700, 500))
    clock = pygame.time.Clock()

    font_big = pygame.font.SysFont(None, 72)
    font_small = pygame.font.SysFont(None, 28)

    hand_img = load_hand_image()

    center = (350, 250)
    radius = 170

    running = True
    while running:
        # Handle exit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        now = dt.datetime.now()
        minute_angle, second_angle = time_to_angles(now)

        screen.fill((220, 235, 245))
        draw_clock_face(screen, center, radius)

        # Right hand = minutes hand
        minute_hand = rotate_hand(hand_img, minute_angle)
        minute_rect = minute_hand.get_rect()
        minute_rect.center = center
        # Position the pivot near the sleeve end by shifting the rendered surface
        minute_rect.center = (center[0] + 20, center[1])
        screen.blit(minute_hand, minute_rect)

        # Left hand = seconds hand
        second_hand = rotate_hand(hand_img, second_angle)
        second_rect = second_hand.get_rect()
        second_rect.center = (center[0] - 20, center[1])
        screen.blit(second_hand, second_rect)

        # Center cap so the hands look anchored
        pygame.draw.circle(screen, (40, 40, 40), center, 8)

        time_text = now.strftime("%M:%S")
        label_text = font_big.render(time_text, True, (20, 20, 20))
        label_rect = label_text.get_rect(center=(350, 60))
        screen.blit(label_text, label_rect)

        info_text = font_small.render("Right hand = minutes | Left hand = seconds", True, (30, 30, 30))
        info_rect = info_text.get_rect(center=(350, 420))
        screen.blit(info_text, info_rect)

        pygame.display.flip()
        clock.tick(1)  # update every second

    pygame.quit()


if __name__ == "__main__":
    main()