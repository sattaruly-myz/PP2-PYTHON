import pygame
import os


class MusicPlayer:
    """
    Manages a playlist of .mp3 / .wav files from a given folder.
    Uses pygame.mixer for playback.
    """

    SUPPORTED_EXT = (".mp3", ".wav")

    def __init__(self, music_folder: str = "music"):
        self.music_folder = music_folder
        self.tracks: list[str] = []
        self.current_index: int = 0
        self.is_playing: bool = False

        self._scan_folder()

    def _scan_folder(self):
        """Find all supported audio files in the music folder."""
        if not os.path.isdir(self.music_folder):
            os.makedirs(self.music_folder)
            print(f"[MusicPlayer] Created empty folder: '{self.music_folder}'")
            return

        for filename in sorted(os.listdir(self.music_folder)):
            if filename.lower().endswith(self.SUPPORTED_EXT):
                self.tracks.append(os.path.join(self.music_folder, filename))

        print(f"[MusicPlayer] Found {len(self.tracks)} track(s).")

    # ---------- Playback controls ----------

    def play(self):
        """Load and play the current track."""
        if not self.tracks:
            return
        pygame.mixer.music.load(self.tracks[self.current_index])
        pygame.mixer.music.play()
        self.is_playing = True

    def stop(self):
        """Stop playback."""
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        """Switch to the next track (wraps around)."""
        if not self.tracks:
            return
        self.current_index = (self.current_index + 1) % len(self.tracks)
        if self.is_playing:
            self.play()

    def prev_track(self):
        """Switch to the previous track (wraps around)."""
        if not self.tracks:
            return
        self.current_index = (self.current_index - 1) % len(self.tracks)
        if self.is_playing:
            self.play()

    # ---------- Info ----------

    def get_track_name(self) -> str:
        """Return the filename of the currently selected track."""
        if not self.tracks:
            return "No tracks found in 'music/' folder"
        return os.path.basename(self.tracks[self.current_index])

    def get_status(self) -> str:
        return "▶  Playing" if self.is_playing else "■  Stopped"