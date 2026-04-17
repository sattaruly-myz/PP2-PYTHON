from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import time
import wave
import contextlib

import pygame


BASE_DIR = Path(__file__).resolve().parent
MUSIC_DIR = BASE_DIR / "music"


def get_audio_duration(path: Path) -> float:
    """Return track duration in seconds when possible."""
    suffix = path.suffix.lower()
    try:
        if suffix == ".wav":
            with contextlib.closing(wave.open(str(path), "rb")) as wf:
                frames = wf.getnframes()
                rate = wf.getframerate()
                return frames / float(rate) if rate else 0.0
    except Exception:
        return 0.0
    return 0.0


@dataclass
class Track:
    path: Path
    duration: float


class MusicPlayer:
    def __init__(self, music_dir: Path):
        self.music_dir = music_dir
        self.tracks: list[Track] = self._scan_tracks()
        self.index = 0
        self.is_playing = False
        self.track_started_at = 0.0

    def _scan_tracks(self) -> list[Track]:
        supported = {".wav", ".mp3", ".ogg"}
        tracks = []
        if self.music_dir.exists():
            for p in sorted(self.music_dir.rglob("*")):
                if p.is_file() and p.suffix.lower() in supported:
                    tracks.append(Track(path=p, duration=get_audio_duration(p)))
        return tracks

    def current(self) -> Track | None:
        if not self.tracks:
            return None
        return self.tracks[self.index]

    def play(self) -> None:
        track = self.current()
        if track is None:
            return
        pygame.mixer.music.load(str(track.path))
        pygame.mixer.music.play()
        self.is_playing = True
        self.track_started_at = time.time()

    def stop(self) -> None:
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self) -> None:
        if not self.tracks:
            return
        self.index = (self.index + 1) % len(self.tracks)
        self.play()

    def previous_track(self) -> None:
        if not self.tracks:
            return
        self.index = (self.index - 1) % len(self.tracks)
        self.play()

    def elapsed(self) -> float:
        if not self.is_playing:
            return 0.0
        return max(0.0, time.time() - self.track_started_at)

    def progress_text(self) -> str:
        track = self.current()
        if track is None:
            return "No audio files found in music_player/music/"

        elapsed = self.elapsed()
        duration = track.duration

        if duration > 0:
            elapsed_int = min(int(elapsed), int(duration))
            duration_int = int(duration)
            return f"{elapsed_int:02d}:{elapsed_int % 60:02d} / {duration_int:02d}:{duration_int % 60:02d}"

        return f"{int(elapsed):02d}s elapsed"

    def handle_track_end(self) -> None:
        if self.is_playing and not pygame.mixer.music.get_busy():
            # Move to the next track automatically when the current one ends.
            self.next_track()


def draw_text(screen: pygame.Surface, font: pygame.font.Font, text: str, x: int, y: int, color=(20, 20, 20)) -> None:
    surf = font.render(text, True, color)
    screen.blit(surf, (x, y))


def main() -> None:
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    pygame.mixer.init()

    pygame.display.set_caption("Music Player with Keyboard Controller")
    screen = pygame.display.set_mode((860, 420))
    clock = pygame.time.Clock()

    font_title = pygame.font.SysFont(None, 44)
    font_ui = pygame.font.SysFont(None, 32)
    font_small = pygame.font.SysFont(None, 24)

    player = MusicPlayer(MUSIC_DIR)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_p:
                    player.play()
                elif event.key == pygame.K_s:
                    player.stop()
                elif event.key == pygame.K_n:
                    player.next_track()
                elif event.key == pygame.K_b:
                    player.previous_track()

        player.handle_track_end()

        screen.fill((245, 245, 245))
        pygame.draw.rect(screen, (220, 230, 255), (25, 25, 810, 370), border_radius=18)

        draw_text(screen, font_title, "Music Player", 50, 45)
        draw_text(screen, font_ui, "P = Play    S = Stop    N = Next    B = Previous    Q = Quit", 50, 100)

        current = player.current()
        if current is None:
            draw_text(screen, font_ui, "No tracks were found.", 50, 160)
            draw_text(screen, font_small, "Place .wav, .mp3, or .ogg files in music_player/music/", 50, 200)
        else:
            draw_text(screen, font_ui, f"Track {player.index + 1} of {len(player.tracks)}", 50, 160)
            draw_text(screen, font_ui, f"Current file: {current.path.name}", 50, 200)
            draw_text(screen, font_ui, f"Status: {'Playing' if player.is_playing else 'Stopped'}", 50, 240)
            draw_text(screen, font_ui, f"Progress: {player.progress_text()}", 50, 280)

            bar_x, bar_y, bar_w, bar_h = 50, 330, 720, 26
            pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_w, bar_h), border_radius=10)
            pygame.draw.rect(screen, (60, 120, 220), (bar_x, bar_y, bar_w // 2, bar_h), border_radius=10)
            pygame.draw.rect(screen, (40, 40, 40), (bar_x, bar_y, bar_w, bar_h), 2, border_radius=10)
            draw_text(screen, font_small, "Playback bar (visual)", bar_x, bar_y - 26)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()