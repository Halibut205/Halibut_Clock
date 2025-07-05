"""
Simple Sound Manager - Fallback without pygame dependency
"""

import os

class SoundManager:
    def __init__(self):
        self.enabled = False
        self.sounds = {}
        self._try_initialize()

    def _try_initialize(self):
        """Thử khởi tạo pygame, fallback nếu không có"""
        try:
            import pygame
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.enabled = True
            self._load_sounds()
            print("✅ Sound system initialized with pygame")
        except ImportError:
            print("🔇 pygame not available - sound effects disabled")
            self.enabled = False
        except Exception as e:
            print(f"🔇 Sound initialization failed: {e}")
            self.enabled = False

    def _load_sounds(self):
        """Load sound files if pygame available"""
        if not self.enabled:
            return
            
        try:
            import pygame
            sfx_dir = os.path.join(os.path.dirname(__file__), "..", "..", "sfx")
            
            sound_files = {
                'button_click': os.path.join(sfx_dir, 'button_1.mp3'),
                'start': os.path.join(sfx_dir, 'button_1.mp3'),
                'pause': os.path.join(sfx_dir, 'button_1.mp3'),
                'reset': os.path.join(sfx_dir, 'button_1.mp3'),
                'session_complete': os.path.join(sfx_dir, 'button_1.mp3')
            }
            
            for sound_name, file_path in sound_files.items():
                if os.path.exists(file_path):
                    self.sounds[sound_name] = pygame.mixer.Sound(file_path)
                    print(f"✅ Loaded sound: {sound_name}")
                    
        except Exception as e:
            print(f"⚠️ Could not load sounds: {e}")
            self.enabled = False

    def play_sound(self, sound_name, volume=0.5):
        """Play sound if available"""
        if not self.enabled or sound_name not in self.sounds:
            return # Silent fallback
            
        try:
            sound = self.sounds[sound_name]
            sound.set_volume(volume)
            sound.play()
        except:
            pass # Silent fallback

    def play_button_click(self):
        """Play button click sound"""
        self.play_sound('button_click', volume=0.3)

    def play_start(self):
        """Play start sound"""
        self.play_sound('start', volume=0.4)

    def play_pause(self):
        """Play pause sound"""
        self.play_sound('pause', volume=0.4)

    def play_reset(self):
        """Play reset sound"""
        self.play_sound('reset', volume=0.4)

    def play_session_complete(self):
        """Play session complete sound"""
        self.play_sound('session_complete', volume=0.6)

    def toggle_sound(self):
        """Toggle sound on/off"""
        if self.enabled:
            self.enabled = False
            return False
        else:
            self._try_initialize()
            return self.enabled

    def set_volume(self, volume):
        """Set volume for all sounds"""
        if not self.enabled:
            return
            
        for sound in self.sounds.values():
            try:
                sound.set_volume(volume)
            except:
                pass
