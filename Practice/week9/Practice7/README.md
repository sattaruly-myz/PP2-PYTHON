# Practice 7: Game Development with Pygame (Part 1) 🎮

This repository contains my solutions for Practice 7, which introduces basic game development concepts using the `pygame` library. The practice is divided into three mini-projects focusing on graphics, input handling, and audio.

## 📁 Repository Structure

The project follows a modular structure, separating each mini-game into its own directory with dedicated classes and assets:

```text
Practice7/
├── mickeys_clock/     # Application 1: Digital-style clock with rotating hands
├── music_player/      # Application 2: Interactive music player with keyboard controls
├── moving_ball/       # Application 3: Interactive game with boundary checking
├── requirements.txt   # Project dependencies
└── README.md          # This file

🚀 How to Run

    Install dependencies:
    Ensure you have Python installed. Then, install the required library:
    code Bash

    pip install -r requirements.txt

    Run individual games:
    Navigate to the specific game folder and execute main.py.
    code Bash

    # Example for Moving Ball:
    cd moving_ball
    python main.py

🎮 Project Details
1. Mickey's Clock (mickeys_clock/)

A real-time clock application.

    Features: Synchronizes with the system clock (datetime.now()). Uses pygame.transform.rotate() to animate Mickey's hands (Right = Minutes, Left = Seconds).

    Note: Ensure mickey_hand.png is present in the images/ directory.

2. Music Player (music_player/)

A keyboard-controlled audio player.

    Controls:

        P - Play

        S - Stop

        N - Next Track

        B - Previous Track

        Q - Quit

    Features: Uses pygame.mixer.music for playback and displays the current track status on the screen.

    Note: Add sample .wav or .mp3 files to the music/ directory before running.

3. Moving Ball Game (moving_ball/)

A simple interactive simulation focusing on boundary logic.

    Features: A red ball (radius 25) controlled by the Arrow Keys (Up, Down, Left, Right). The ball moves 20 pixels per keystroke and includes strict boundary checking to prevent it from leaving the 800x600 screen.

Developed as part of the Principles of Programming II course.
code Code

---

### 📝 Файл: `Practice7/requirements.txt`
*(Это тоже требуется в задании. Создай этот файл и вставь туда одну строчку):*

```text
pygame>=2.0.0