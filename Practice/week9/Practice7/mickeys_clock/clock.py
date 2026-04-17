"""Clock helpers for Mickey's Clock."""

from __future__ import annotations

import datetime as dt
import math
from pathlib import Path

import pygame


BASE_DIR = Path(__file__).resolve().parent
ASSET_PATH = BASE_DIR / "images" / "mickey_hand.png"


def load_hand_image() -> pygame.Surface:
    if ASSET_PATH.exists():
        return pygame.image.load(str(ASSET_PATH)).convert_alpha()
    surface = pygame.Surface((220, 80), pygame.SRCALPHA)
    pygame.draw.rect(surface, (180, 30, 30), (0, 20, 140, 40), border_radius=12)
    pygame.draw.rect(surface, (255, 225, 190), (120, 12, 85, 56), border_radius=18)
    pygame.draw.circle(surface, (255, 225, 190), (198, 40), 10)
    return surface


def rotate_hand(image: pygame.Surface, angle_deg: float) -> pygame.Surface:
    return pygame.transform.rotate(image, -angle_deg)


def time_to_angles(now: dt.datetime) -> tuple[float, float]:
    seconds = now.second + now.microsecond / 1_000_000
    minutes = now.minute + seconds / 60.0
    return minutes * 6.0, seconds * 6.0