"""
Enhanced Sound Manager - Button sounds + Background music with volume control
"""

import os
import pygame

class SoundManager:
    """Quản lý âm thanh button + background music với pygame"""
    
    def __init__(self):
        self.sound_enabled = False
        self.button_sound = None
        self.background_music_file = None
        self.music_volume = 0.3  # Default volume (30%)
        self.button_volume = 0.7  # Button volume (70%)
        self.music_playing = False
        self._init_pygame()
    
    def _init_pygame(self):
        """Khởi tạo pygame mixer"""
        try:
            # Initialize mixer with better settings for music
            pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=1024)
            pygame.mixer.init()
            self._load_sounds()
            self.sound_enabled = True
            print("[SOUND] Pygame initialized successfully")
        except Exception as e:
            print(f"[SOUND] Could not initialize pygame: {e}")
            self.sound_enabled = False
    
    def _load_sounds(self):
        """Load tất cả sound files"""
        # Load button sound
        button_file = os.path.join("sfx", "button_1.mp3")
        if os.path.exists(button_file):
            try:
                self.button_sound = pygame.mixer.Sound(button_file)
                self.button_sound.set_volume(self.button_volume)
                print(f"[SOUND] Loaded button sound: {button_file}")
            except Exception as e:
                print(f"[SOUND] Could not load button sound {button_file}: {e}")
                self.button_sound = None
        else:
            print(f"[SOUND] Button sound file not found: {button_file}")
            self.button_sound = None
        
        # Check for background music
        music_file = os.path.join("sfx", "whitenoise_1.mp3")
        if os.path.exists(music_file):
            self.background_music_file = music_file
            print(f"[SOUND] Found background music: {music_file}")
        else:
            print(f"[SOUND] Background music file not found: {music_file}")
            self.background_music_file = None
    
    def play_button_click(self):
        """Phát âm thanh khi click button"""
        if self.sound_enabled and self.button_sound:
            try:
                self.button_sound.play()
            except Exception as e:
                print(f"[SOUND] Error playing button sound: {e}")
    
    def start_background_music(self):
        """Bắt đầu phát background music (loop)"""
        if not self.sound_enabled or not self.background_music_file:
            return
        
        try:
            if not self.music_playing:
                pygame.mixer.music.load(self.background_music_file)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1)  # -1 means loop forever
                self.music_playing = True
                print(f"[SOUND] Started background music (volume: {int(self.music_volume * 100)}%)")
        except Exception as e:
            print(f"[SOUND] Error starting background music: {e}")
    
    def pause_background_music(self):
        """Tạm dừng background music"""
        if self.sound_enabled and self.music_playing:
            try:
                pygame.mixer.music.pause()
                print("[SOUND] Background music paused")
            except Exception as e:
                print(f"[SOUND] Error pausing background music: {e}")
    
    def resume_background_music(self):
        """Tiếp tục background music"""
        if self.sound_enabled and self.music_playing:
            try:
                pygame.mixer.music.unpause()
                print("[SOUND] Background music resumed")
            except Exception as e:
                print(f"[SOUND] Error resuming background music: {e}")
    
    def stop_background_music(self):
        """Dừng background music"""
        if self.sound_enabled:
            try:
                pygame.mixer.music.stop()
                self.music_playing = False
                print("[SOUND] Background music stopped")
            except Exception as e:
                print(f"[SOUND] Error stopping background music: {e}")
    
    def set_music_volume(self, volume):
        """Đặt volume cho background music (0.0 - 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        if self.sound_enabled and self.music_playing:
            try:
                pygame.mixer.music.set_volume(self.music_volume)
                print(f"[SOUND] Music volume set to {int(self.music_volume * 100)}%")
            except Exception as e:
                print(f"[SOUND] Error setting music volume: {e}")
    
    def set_button_volume(self, volume):
        """Đặt volume cho button sounds (0.0 - 1.0)"""
        self.button_volume = max(0.0, min(1.0, volume))
        if self.button_sound:
            try:
                self.button_sound.set_volume(self.button_volume)
                print(f"[SOUND] Button volume set to {int(self.button_volume * 100)}%")
            except Exception as e:
                print(f"[SOUND] Error setting button volume: {e}")
    
    def get_music_volume(self):
        """Lấy music volume hiện tại"""
        return self.music_volume
    
    def get_button_volume(self):
        """Lấy button volume hiện tại"""
        return self.button_volume
    
    def is_music_available(self):
        """Kiểm tra xem background music có khả dụng không"""
        return self.sound_enabled and self.background_music_file is not None
    
    def is_music_playing(self):
        """Kiểm tra xem music có đang play không"""
        return self.music_playing
    
    def cleanup(self):
        """Dọn dẹp resources"""
        try:
            if self.sound_enabled:
                self.stop_background_music()
                pygame.mixer.quit()
        except:
            pass

# Backward compatibility
ButtonSoundManager = SoundManager
