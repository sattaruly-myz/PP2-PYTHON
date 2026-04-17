from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import contextlib
import time
import wave

import pygame


@dataclass
class Track:
    path: Path
    duration: float


class MusicPlayer:
    def __init__(self, music_dir: Path):
        self.music_dir = music_dir
        self.tracks = self._scan_tracks()
        self.index = 0
        self.is_playing = False
        self.track_started_at = 0.0

    def _scan_tracks(self) -> list[Track]:
        supported = {".wav", ".mp3", ".ogg"}
        tracks: list[Track] = []
        if self.music_dir.exists():
            for p in sorted(self.music_dir.rglob("*")):
                if p.is_file() and p.suffix.lower() in supported:
                    tracks.append(Track(p, self._duration(p)))
        return tracks

    def _duration(self, path: Path) -> float:
        try:
            if path.suffix.lower() == ".wav":
                with contextlib.closing(wave.open(str(path), "rb")) as wf:
                    return wf.getnframes() / float(wf.getframerate())
        except Exception:
            pass
        return 0.0

    def current(self) -> Track | None:
        return self.tracks[self.index] if self.tracks else None

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
        if self.tracks:
            self.index = (self.index + 1) % len(self.tracks)
            self.play()

    def previous_track(self) -> None:
        if self.tracks:
            self.index = (self.index - 1) % len(self.tracks)
            self.play()

    def elapsed(self) -> float:
        return max(0.0, time.time() - self.track_started_at) if self.is_playing else 0.0