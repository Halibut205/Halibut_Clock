"""
Simple Sound Manager - Chỉ sử dụng pygame cho button sounds
"""

import os
import pygame

class ButtonSoundManager:
    """Quản lý âm thanh button đơn giản với pygame"""
    
    def __init__(self):
        self.sound_enabled = False
        self.button_sound = None
        self._init_pygame()
    
    def _init_pygame(self):
        """Khởi tạo pygame mixer"""
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self._load_button_sound()
            self.sound_enabled = True
            print("[SOUND] Pygame initialized successfully")
        except Exception as e:
            print(f"[SOUND] Could not initialize pygame: {e}")
            self.sound_enabled = False
    
    def _load_button_sound(self):
        """Load sound file cho button"""
        sound_file = os.path.join("sfx", "button_1.mp3")
        if os.path.exists(sound_file):
            try:
                self.button_sound = pygame.mixer.Sound(sound_file)
                print(f"[SOUND] Loaded: {sound_file}")
            except Exception as e:
                print(f"[SOUND] Could not load {sound_file}: {e}")
                self.button_sound = None
        else:
            print(f"[SOUND] Sound file not found: {sound_file}")
            self.button_sound = None
    
    def play_button_click(self):
        """Phát âm thanh khi click button"""
        if self.sound_enabled and self.button_sound:
            try:
                self.button_sound.play()
            except Exception as e:
                print(f"[SOUND] Error playing button sound: {e}")
    
    def cleanup(self):
        """Dọn dẹp resources"""
        try:
            if self.sound_enabled:
                pygame.mixer.quit()
        except:
            pass
