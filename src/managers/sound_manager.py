"""
Sound Manager - Complete pygame implementation
"""

import os
from typing import Optional

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("[SOUND] pygame not available. Install with: pip install pygame")


class SoundManager:
    """Complete sound manager using pygame for all audio functionality"""
    
    def __init__(self):
        self.sound_enabled = False
        self.music_muted = False
        self.volume_before_mute = 0.3
        
        # Sound objects
        self.button_main_sound: Optional['pygame.mixer.Sound'] = None
        self.button_secondary_sound: Optional['pygame.mixer.Sound'] = None
        self.button_stat_sound: Optional['pygame.mixer.Sound'] = None
        self.completion_sound: Optional['pygame.mixer.Sound'] = None
        self.background_music_file: Optional[str] = None
        
        # Volume settings
        self.music_volume = 0.3  # Default volume (30%)
        self.button_volume = 0.7  # Button volume (70%)
        self.music_playing = False
        
        # Initialize pygame if available
        if PYGAME_AVAILABLE:
            self._init_pygame()
    
    def _init_pygame(self):
        """Initialize pygame mixer with optimized settings"""
        try:
            # Initialize mixer with better settings for music
            pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=1024)
            pygame.mixer.init()
            self._load_sounds()
            self.sound_enabled = True
            print("[SOUND] pygame mixer initialized successfully")
        except Exception as e:
            print(f"[SOUND] Could not initialize pygame: {e}")
            self.sound_enabled = False
    
    def _load_sounds(self):
        """Load all sound files with their specific purposes"""
        # Load main button sound (button_1.mp3) - for primary buttons
        button_main_file = os.path.join("sfx", "button_1.mp3")
        if os.path.exists(button_main_file):
            try:
                self.button_main_sound = pygame.mixer.Sound(button_main_file)
                self.button_main_sound.set_volume(self.button_volume)
                print(f"[SOUND] Loaded main button sound: {button_main_file}")
            except Exception as e:
                print(f"[SOUND] Could not load main button sound {button_main_file}: {e}")
                self.button_main_sound = None
        
        # Load secondary button sound (button_2.mp3) - for secondary buttons
        button_secondary_file = os.path.join("sfx", "button_2.mp3")
        if os.path.exists(button_secondary_file):
            try:
                self.button_secondary_sound = pygame.mixer.Sound(button_secondary_file)
                self.button_secondary_sound.set_volume(self.button_volume)
                print(f"[SOUND] Loaded secondary button sound: {button_secondary_file}")
            except Exception as e:
                print(f"[SOUND] Could not load secondary button sound {button_secondary_file}: {e}")
                self.button_secondary_sound = None
        
        # Load stats button sound (button_stat.mp3) - for daily stats button
        button_stat_file = os.path.join("sfx", "button_stat.mp3")
        if os.path.exists(button_stat_file):
            try:
                self.button_stat_sound = pygame.mixer.Sound(button_stat_file)
                self.button_stat_sound.set_volume(self.button_volume)
                print(f"[SOUND] Loaded stats button sound: {button_stat_file}")
            except Exception as e:
                print(f"[SOUND] Could not load stats button sound {button_stat_file}: {e}")
                self.button_stat_sound = None
        
        # Load session completion sound (rang.mp3)
        completion_file = os.path.join("sfx", "rang.mp3")
        if os.path.exists(completion_file):
            try:
                self.completion_sound = pygame.mixer.Sound(completion_file)
                self.completion_sound.set_volume(self.button_volume)
                print(f"[SOUND] Loaded completion sound: {completion_file}")
            except Exception as e:
                print(f"[SOUND] Could not load completion sound {completion_file}: {e}")
                self.completion_sound = None
        
        # Check for background music (whitenoise_1.mp3)
        music_file = os.path.join("sfx", "whitenoise_1.mp3")
        if os.path.exists(music_file):
            self.background_music_file = music_file
            print(f"[SOUND] Found background music: {music_file}")
        else:
            self.background_music_file = None
            print("[SOUND] No background music file found")
    
    def initialize(self):
        """Initialize sound system (for backward compatibility)"""
        if not PYGAME_AVAILABLE:
            print("[SOUND] pygame not available, sound system disabled")
            return
        
        if not self.sound_enabled:
            self._init_pygame()
    
    # Button sound methods
    def play_button_main(self):
        """Play main button click sound (button_1.mp3)"""
        if self.sound_enabled and self.button_main_sound:
            try:
                self.button_main_sound.play()
            except Exception as e:
                print(f"[SOUND] Error playing main button sound: {e}")
    
    def play_button_secondary(self):
        """Play secondary button click sound (button_2.mp3)"""
        if self.sound_enabled and self.button_secondary_sound:
            try:
                self.button_secondary_sound.play()
            except Exception as e:
                print(f"[SOUND] Error playing secondary button sound: {e}")
    
    def play_button_stat(self):
        """Play stats button click sound (button_stat.mp3)"""
        if self.sound_enabled and self.button_stat_sound:
            try:
                self.button_stat_sound.play()
            except Exception as e:
                print(f"[SOUND] Error playing stats button sound: {e}")
    
    # Backward compatibility method
    def play_button_click(self):
        """Play main button click sound (backward compatibility)"""
        self.play_button_main()
    
    def play_completion_sound(self):
        """Play session completion sound (backward compatibility)"""
        self.play_session_complete()
    
    # Convenience methods for different button types
    def play_main_button_sound(self):
        """Play sound for main action buttons (START, PAUSE/RESUME)"""
        self.play_button_main()
    
    def play_secondary_button_sound(self):
        """Play sound for secondary buttons (RESET, Help, Mute)"""
        self.play_button_secondary()
    
    def play_session_complete(self):
        """Play session completion sound (rang.mp3)"""
        if self.sound_enabled and self.completion_sound:
            try:
                self.completion_sound.play()
                print("[SOUND] Playing session completion sound")
            except Exception as e:
                print(f"[SOUND] Error playing completion sound: {e}")
    
    # Background music methods
    def start_background_music(self):
        """Start background music (whitenoise_1.mp3) with loop"""
        if not self.sound_enabled or not self.background_music_file:
            return
        
        try:
            if not self.music_playing:
                pygame.mixer.music.load(self.background_music_file)
                pygame.mixer.music.set_volume(self.music_volume if not self.music_muted else 0.0)
                pygame.mixer.music.play(-1)  # -1 means loop forever
                self.music_playing = True
                print("[SOUND] Started background music")
        except Exception as e:
            print(f"[SOUND] Error starting background music: {e}")
    
    def stop_background_music(self):
        """Stop background music (called when session ends)"""
        if self.sound_enabled:
            try:
                pygame.mixer.music.stop()
                self.music_playing = False
                print("[SOUND] Stopped background music")
            except Exception as e:
                print(f"[SOUND] Error stopping background music: {e}")
    
    def pause_background_music(self):
        """Pause background music"""
        if self.sound_enabled and self.music_playing:
            try:
                pygame.mixer.music.pause()
                print("[SOUND] Paused background music")
            except Exception as e:
                print(f"[SOUND] Error pausing background music: {e}")
    
    def resume_background_music(self):
        """Resume background music"""
        if self.sound_enabled and self.music_playing:
            try:
                pygame.mixer.music.unpause()
                print("[SOUND] Resumed background music")
            except Exception as e:
                print(f"[SOUND] Error resuming background music: {e}")
    
    # Volume and mute control methods
    def set_music_volume(self, volume):
        """Set volume for background music (0.0 - 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        # Update volume_before_mute if not currently muted
        if not self.music_muted:
            self.volume_before_mute = self.music_volume
        
        if self.sound_enabled and self.music_playing and not self.music_muted:
            try:
                pygame.mixer.music.set_volume(self.music_volume)
            except Exception as e:
                print(f"[SOUND] Error setting music volume: {e}")

    def mute_background_music(self):
        """Mute background music while keeping it playing"""
        if self.sound_enabled and self.music_playing and not self.music_muted:
            try:
                self.volume_before_mute = self.music_volume
                pygame.mixer.music.set_volume(0.0)
                self.music_muted = True
                print("[SOUND] Background music muted")
            except Exception as e:
                print(f"[SOUND] Error muting background music: {e}")

    def unmute_background_music(self):
        """Unmute background music and restore previous volume"""
        if self.sound_enabled and self.music_playing and self.music_muted:
            try:
                pygame.mixer.music.set_volume(self.volume_before_mute)
                self.music_muted = False
                print("[SOUND] Background music unmuted")
            except Exception as e:
                print(f"[SOUND] Error unmuting background music: {e}")

    def toggle_mute_background_music(self):
        """Toggle mute/unmute background music"""
        if self.music_muted:
            self.unmute_background_music()
        else:
            self.mute_background_music()
        return self.music_muted
    
    # Backward compatibility methods
    def toggle_mute(self):
        """Toggle mute state (backward compatibility)"""
        return self.toggle_mute_background_music()
        
    def set_mute(self, muted: bool):
        """Set mute state (backward compatibility)"""
        if muted and not self.music_muted:
            self.mute_background_music()
        elif not muted and self.music_muted:
            self.unmute_background_music()
    
    def set_button_volume(self, volume):
        """Set volume for button sounds (0.0 - 1.0)"""
        self.button_volume = max(0.0, min(1.0, volume))
        
        # Update all button sounds volume
        if self.button_main_sound:
            try:
                self.button_main_sound.set_volume(self.button_volume)
            except Exception as e:
                print(f"[SOUND] Error setting main button volume: {e}")
        
        if self.button_secondary_sound:
            try:
                self.button_secondary_sound.set_volume(self.button_volume)
            except Exception as e:
                print(f"[SOUND] Error setting secondary button volume: {e}")
        
        if self.button_stat_sound:
            try:
                self.button_stat_sound.set_volume(self.button_volume)
            except Exception as e:
                print(f"[SOUND] Error setting stats button volume: {e}")
        
        if self.completion_sound:
            try:
                self.completion_sound.set_volume(self.button_volume)
            except Exception as e:
                print(f"[SOUND] Error setting completion volume: {e}")
    
    # Status and information methods
    def get_music_volume(self):
        """Get current music volume"""
        return self.music_volume
    
    def get_button_volume(self):
        """Get current button volume"""
        return self.button_volume
    
    def is_music_available(self):
        """Check if background music is available"""
        return self.sound_enabled and self.background_music_file is not None
    
    def is_music_playing(self):
        """Check if music is currently playing"""
        return self.music_playing

    def is_music_muted(self):
        """Check if music is currently muted"""
        return self.music_muted

    def get_mute_status(self):
        """Get mute status and volume information"""
        return {
            "muted": self.music_muted,
            "current_volume": self.music_volume if not self.music_muted else 0.0,
            "volume_before_mute": self.volume_before_mute
        }
    
    def cleanup(self):
        """Clean up pygame resources"""
        try:
            if self.sound_enabled:
                self.stop_background_music()
                pygame.mixer.quit()
                print("[SOUND] Cleaned up pygame resources")
        except:
            pass


# Backward compatibility
ButtonSoundManager = SoundManager
