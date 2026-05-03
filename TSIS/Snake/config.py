WINDOW_W = 800
WINDOW_H = 640
HUD_H = 40
GRID = 20
COLS = WINDOW_W // GRID
ROWS = (WINDOW_H - HUD_H) // GRID
FPS = 60
BASE_SPEED = 8
FOOD_PER_LEVEL = 5
import os
from dotenv import load_dotenv
load_dotenv()
DB_DSN = (
f"host={os.getenv('DB_HOST', 'localhost')} "
f"port={os.getenv('DB_PORT', '5432')} "
f"dbname={os.getenv('DB_NAME', 'snake_game')} "
f"user={os.getenv('DB_USER', 'postgres')} "
f"password={os.getenv('DB_PASSWORD', '')}"
)