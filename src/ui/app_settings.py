"""
Settings cho welcome screen
"""

import os
import json

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'app_settings.json')

def load_settings():
    """Load app settings"""
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    
    # Default settings
    return {
        'show_welcome': True,
        'first_run': True
    }

def save_settings(settings):
    """Save app settings"""
    try:
        os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2)
    except:
        pass

def should_show_welcome():
    """Check if should show welcome screen"""
    settings = load_settings()
    return settings.get('show_welcome', True)

def mark_welcome_shown():
    """Mark that welcome screen has been shown"""
    settings = load_settings()
    settings['show_welcome'] = False
    settings['first_run'] = False
    save_settings(settings)

def reset_welcome():
    """Reset welcome screen to show again"""
    settings = load_settings()
    settings['show_welcome'] = True
    save_settings(settings)
