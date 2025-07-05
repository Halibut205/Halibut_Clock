# -*- coding: utf-8 -*-
"""
Cross-Platform Sound Manager - Optimized for Windows, macOS, Linux
"""

import os
import platform
import threading

class SoundManager:
    def __init__(self):
        self.enabled = False
        self.engine = None
        self.sound_files = {}
        self._initialize()
        
    def _initialize(self):
        """Initialize sound engine with smart fallback system"""
        # Try engines in priority order
        engines = [
            ('pygame', self._init_pygame),
            ('playsound', self._init_playsound), 
            ('system', self._init_system_beep)
        ]
        
        for name, init_func in engines:
            if init_func():
                self.engine = name
                break
        
        if self.enabled:
            self._load_sound_files()
            print(f"🔊 Audio: {self.engine}")
        else:
            print("🔇 No audio available")
    
    def _init_pygame(self):
        """Try pygame initialization"""
        try:
            import pygame
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.enabled = True
            return True
        except:
            return False
    
    def _init_playsound(self):
        """Try playsound initialization"""
        try:
            import playsound
            self.enabled = True
            return True
        except:
            return False
    
    def _init_system_beep(self):
        """Initialize system beep fallback"""
        system = platform.system()
        if system == "Windows":
            try:
                import winsound
                self.enabled = True
                return True
            except:
                pass
        elif system in ["Darwin", "Linux"]:
            self.enabled = True
            return True
        return False
    
    def _load_sound_files(self):
        """Load sound files for file-based engines"""
        if self.engine in ['pygame', 'playsound']:
            sfx_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'sfx')
            sound_file = os.path.join(sfx_dir, 'button_1.mp3')
            
            if os.path.exists(sound_file):
                self.sound_files['click'] = sound_file
                print(f"✅ Loaded: {sound_file}")
    
    def play_sound(self, sound_type='click'):
        """Play sound with current engine"""
        if not self.enabled:
            return
            
        try:
            if self.engine == 'pygame':
                self._play_pygame(sound_type)
            elif self.engine == 'playsound':
                self._play_playsound(sound_type)
            elif self.engine == 'system':
                self._play_system_beep()
        except Exception as e:
            print(f"⚠️ Audio error: {e}")
    
    def _play_pygame(self, sound_type):
        """Play with pygame"""
        if sound_type in self.sound_files:
            import pygame
            sound = pygame.mixer.Sound(self.sound_files[sound_type])
            sound.play()
    
    def _play_playsound(self, sound_type):
        """Play with playsound (non-blocking)"""
        if sound_type in self.sound_files:
            def play():
                try:
                    from playsound import playsound
                    playsound(self.sound_files[sound_type], block=False)
                except:
                    pass
            
            thread = threading.Thread(target=play, daemon=True)
            thread.start()
    
    def _play_system_beep(self):
        """Play system beep"""
        system = platform.system()
        try:
            if system == "Windows":
                import winsound
                winsound.Beep(800, 150)
            elif system == "Darwin":
                os.system("afplay /System/Library/Sounds/Pop.aiff")
            elif system == "Linux":
                os.system("beep -f 800 -l 150 2>/dev/null || echo -e '\a'")
        except:
            pass
    
    # Public API
    def play_button_click(self):
        """Play button click sound"""
        self.play_sound('click')
    
    def play_session_complete(self):
        """Play session complete sound"""
        self.play_sound('click')
    
    def play_break_time(self):
        """Play break time sound"""
        self.play_sound('click')
    
    def toggle_sound(self):
        """Toggle sound on/off"""
        self.enabled = not self.enabled
        return self.enabled
    
    def is_enabled(self):
        """Check if sound is enabled"""
        return self.enabled
