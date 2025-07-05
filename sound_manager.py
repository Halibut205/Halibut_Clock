"""
Sound Effects Module - Quản lý âm thanh cho ứng dụng
"""

import pygame
import os

class SoundManager:
    def __init__(self):
        self.enabled = True
        self.sounds = {}
        self._initialize_pygame()
        self._load_sounds()

    def _initialize_pygame(self):
        """Khởi tạo pygame mixer cho âm thanh"""
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            print("✅ Sound system initialized")
        except Exception as e:
            print(f"❌ Could not initialize sound system: {e}")
            self.enabled = False

    def _load_sounds(self):
        """Load các file âm thanh"""
        if not self.enabled:
            return
            
        sound_files = {
            'button_click': 'sfx/button_1.mp3',
            'start': 'sfx/button_1.mp3',
            'pause': 'sfx/button_1.mp3',
            'reset': 'sfx/button_1.mp3',
            'session_complete': 'sfx/button_1.mp3'
        }
        
        for sound_name, file_path in sound_files.items():
            try:
                if os.path.exists(file_path):
                    self.sounds[sound_name] = pygame.mixer.Sound(file_path)
                    print(f"✅ Loaded sound: {sound_name}")
                else:
                    print(f"⚠️ Sound file not found: {file_path}")
            except Exception as e:
                print(f"❌ Could not load sound {sound_name}: {e}")

    def play_sound(self, sound_name, volume=0.5):
        """Phát âm thanh"""
        if not self.enabled or sound_name not in self.sounds:
            return
            
        try:
            sound = self.sounds[sound_name]
            sound.set_volume(volume)
            sound.play()
        except Exception as e:
            print(f"❌ Could not play sound {sound_name}: {e}")

    def play_button_click(self):
        """Phát âm thanh khi bấm nút"""
        self.play_sound('button_click', volume=0.3)

    def play_start(self):
        """Phát âm thanh khi start"""
        self.play_sound('start', volume=0.4)

    def play_pause(self):
        """Phát âm thanh khi pause"""
        self.play_sound('pause', volume=0.4)

    def play_reset(self):
        """Phát âm thanh khi reset"""
        self.play_sound('reset', volume=0.4)

    def play_session_complete(self):
        """Phát âm thanh khi hoàn thành session"""
        self.play_sound('session_complete', volume=0.6)

    def toggle_sound(self):
        """Bật/tắt âm thanh"""
        self.enabled = not self.enabled
        return self.enabled

    def set_volume(self, volume):
        """Điều chỉnh âm lượng chung (0.0 - 1.0)"""
        if not self.enabled:
            return
            
        for sound in self.sounds.values():
            sound.set_volume(volume)
