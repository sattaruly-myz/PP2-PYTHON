# Music Player

A keyboard-controlled music player built with pygame.mixer.

## Setup
1. Place your `.mp3` or `.wav` files inside the `music/` folder.
2. Install dependencies and run:

```bash
pip install pygame
python main.py
```

## Controls
| Key | Action          |
|-----|-----------------|
| P   | Play            |
| S   | Stop            |
| N   | Next track      |
| B   | Previous track  |
| Q   | Quit            |

## Notes
- Tracks are sorted alphabetically.
- If `music/` folder is empty, the player will show "No tracks found".