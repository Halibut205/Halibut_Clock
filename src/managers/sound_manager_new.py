# -*- coding: utf-8 -*-
"""
Cross-Platform Sound Manager - Hỗ trợ Windows, macOS, Linux
"""

import os
import platform
import threading

class SoundManager:
    def __init__(self):
        self.enabled = False
        self.sound_engine = None
        self.sound_files = {}
        self._initialize()
        
    def _initialize(self):
        """Khởi tạo sound engine theo platform"""
        system = platform.system()
        
        # Thử các engine theo thứ tự ưu tiên
        engines = [
            self._try_playsound,
            self._try_pygame,
            self._try_system_beep
        ]
        
        for engine in engines:
            if engine():
                break
        
        if self.enabled:
            self._load_sound_files()
        else:
            print("🔇 No sound engine available")
    
    def _try_playsound(self):
        """Thử sử dụng playsound (cross-platform)"""
        try:
            import playsound
            self.sound_engine = "playsound"
            self.enabled = True
            print("🔊 Sound engine: playsound (cross-platform)")
            return True
        except ImportError:
            return False
    
    def _try_pygame(self):
        """Thử sử dụng pygame"""
        try:
            import pygame
            pygame.mixer.init()
            self.sound_engine = "pygame"
            self.enabled = True
            print("🔊 Sound engine: pygame")
            return True
        except (ImportError, Exception):
            return False
    
    def _try_system_beep(self):
        """Fallback sang system beep"""
        system = platform.system()
        
        if system == "Windows":
            try:
                import winsound
                self.sound_engine = "winsound"
                self.enabled = True
                print("🔊 Sound engine: Windows beep")
                return True
            except ImportError:
                pass
        
        elif system == "Darwin":  # macOS
            self.sound_engine = "macos_beep"
            self.enabled = True
            print("🔊 Sound engine: macOS beep")
            return True
            
        elif system == "Linux":
            self.sound_engine = "linux_beep"
            self.enabled = True
            print("🔊 Sound engine: Linux beep")
            return True
        
        return False
    
    def _load_sound_files(self):
        """Load sound files cho các engine hỗ trợ file"""
        if self.sound_engine in ["playsound", "pygame"]:
            sfx_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'sfx')
            
            sound_map = {
                'button_click': 'button_1.mp3',
                'session_complete': 'button_1.mp3',
                'break_time': 'button_1.mp3'
            }
            
            for sound_name, filename in sound_map.items():
                filepath = os.path.join(sfx_dir, filename)
                if os.path.exists(filepath):
                    self.sound_files[sound_name] = filepath
                    print(f"✅ Loaded: {sound_name}")
    
    def play_sound(self, sound_name):
        """Play sound theo engine hiện tại"""
        if not self.enabled:
            return
            
        try:
            if self.sound_engine == "playsound":
                self._play_playsound(sound_name)
            elif self.sound_engine == "pygame":
                self._play_pygame(sound_name)
            else:
                self._play_system_beep()
        except Exception as e:
            print(f"⚠️ Sound error: {e}")
    
    def _play_playsound(self, sound_name):
        """Play với playsound"""
        if sound_name in self.sound_files:
            def play():
                try:
                    from playsound import playsound
                    playsound(self.sound_files[sound_name], block=False)
                except:
                    pass
            
            # Chạy trong thread để không block UI
            thread = threading.Thread(target=play)
            thread.daemon = True
            thread.start()
    
    def _play_pygame(self, sound_name):
        """Play với pygame"""
        if sound_name in self.sound_files:
            try:
                import pygame
                sound = pygame.mixer.Sound(self.sound_files[sound_name])
                sound.play()
            except:
                pass
    
    def _play_system_beep(self):
        """Play system beep"""
        try:
            if self.sound_engine == "winsound":
                import winsound
                winsound.Beep(800, 200)  # 800Hz, 200ms
            
            elif self.sound_engine == "macos_beep":
                import subprocess
                subprocess.run(['say', 'beep'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            elif self.sound_engine == "linux_beep":
                import subprocess
                subprocess.run(['beep'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass
    
    def play_button_click(self):
        """Play button click sound"""
        self.play_sound('button_click')
    
    def play_session_complete(self):
        """Play session complete sound"""
        self.play_sound('session_complete')
    
    def play_break_time(self):
        """Play break time sound"""
        self.play_sound('break_time')
    
    def toggle_sound(self):
        """Toggle sound on/off"""
        self.enabled = not self.enabled
        status = "enabled" if self.enabled else "disabled"
        print(f"🔊 Sound {status}")
        return self.enabled
    
    def is_enabled(self):
        """Check if sound is enabled"""
        return self.enabled
