import json
import os

SETTINGS_FILE = 'settings.json'
LEADERBOARD_FILE = 'leaderboard.json'

DEFAULT_SETTINGS = {
    'sound': False,
    'car_color': 'red',
    'difficulty': 'normal'
}


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE) as f:
                data = json.load(f)
            for k, v in DEFAULT_SETTINGS.items():
                if k not in data:
                    data[k] = v
            return data
        except Exception:
            pass
    return dict(DEFAULT_SETTINGS)


def save_settings(s):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(s, f, indent=2)


def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return []


def save_leaderboard(lb):
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(lb, f, indent=2)


def add_score(name, score, distance):
    lb = load_leaderboard()
    lb.append({'name': name, 'score': score, 'distance': distance})
    lb.sort(key=lambda x: x['score'], reverse=True)
    lb = lb[:10]
    save_leaderboard(lb)
    return lb