"""
Configuration module for Fliqlo Timer
"""

import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, 'src')
DATA_DIR = os.path.join(BASE_DIR, 'data')
SFX_DIR = os.path.join(BASE_DIR, 'sfx')

# Timer settings
DEFAULT_SESSION_DURATION = 3600  # 1 hour in seconds
DEFAULT_TARGET_SESSIONS = 8
DEFAULT_AUTO_CONTINUE = True

# Session duration options (in seconds)
SESSION_DURATION_OPTIONS = {
    "15 min": 15 * 60,    # 900 seconds
    "25 min": 25 * 60,    # 1500 seconds (Pomodoro)
    "30 min": 30 * 60,    # 1800 seconds
    "45 min": 45 * 60,    # 2700 seconds
    "1 hour": 60 * 60,    # 3600 seconds (default)
    "1.5 hours": 90 * 60, # 5400 seconds
    "2 hours": 120 * 60   # 7200 seconds
}

# UI settings
WINDOW_SIZE = "500x600"
WINDOW_TITLE = "Fliqlo Timer"
WINDOW_RESIZABLE = False

# Colors
UI_COLORS = {
    'background': 'black',
    'text': 'white',
    'timer': 'white',
    'break': 'cyan',
    'session': 'yellow',
    'progress': 'orange',
    'button_start': 'green',
    'button_pause': 'orange',
    'button_resume': 'blue',
    'button_reset': 'red'
}

# Fonts
FONTS = {
    'clock': ('Courier New', 36, 'bold'),
    'break': ('Courier New', 18, 'bold'),
    'info': ('Courier New', 12, 'bold'),
    'button': ('Arial', 14, 'bold'),
    'small': ('Arial', 9),
    'tiny': ('Arial', 8)
}

# Sound settings
SOUND_VOLUME = {
    'button_click': 0.3,
    'start': 0.4,
    'pause': 0.4,
    'reset': 0.4,
    'session_complete': 0.6
}

# Data files
TASKS_FILE = os.path.join(DATA_DIR, 'tasks_data.json')
SOUND_FILE = os.path.join(SFX_DIR, 'button_1.mp3')
