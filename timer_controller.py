"""
Timer Controller Module - Điều phối giữa UI và Timer Core
"""

import tkinter as tk
from timer_core import TimerCore
from ui_components import FliqloUI
from sound_manager import SoundManager

class TimerController:
    def __init__(self, root):
        self.root = root
        
        # Khởi tạo core logic, UI và sound
        self.timer_core = TimerCore()
        self.ui = FliqloUI(root)
        self.sound_manager = SoundManager()
        
        # Kết nối callbacks
        self._setup_callbacks()
        
        # Bắt đầu update loop
        self._update_loop()

    def _setup_callbacks(self):
        """Thiết lập callbacks giữa UI và Core"""
        # UI callbacks
        self.ui.on_start = self._handle_start
        self.ui.on_toggle = self._handle_toggle
        self.ui.on_reset = self._handle_reset
        
        # Sound callback
        self.ui.play_sound = self.sound_manager.play_sound
        
        # Core callbacks
        self.timer_core.on_timer_update = self.ui.update_timer_display
        self.timer_core.on_break_update = self.ui.update_break_display
        self.timer_core.on_state_change = self.ui.update_button_state

    def _handle_start(self):
        """Xử lý sự kiện Start"""
        self.timer_core.start_timer()

    def _handle_toggle(self):
        """Xử lý sự kiện Pause/Resume"""
        if self.timer_core.running:
            self.timer_core.pause_timer()
        else:
            self.timer_core.resume_timer()

    def _handle_reset(self):
        """Xử lý sự kiện Reset"""
        self.timer_core.reset_timer()

    def _update_loop(self):
        """Vòng lặp cập nhật timer mỗi giây"""
        self.timer_core.tick()
        # Lặp lại sau 1 giây
        self.root.after(1000, self._update_loop)

    def get_timer_state(self):
        """Lấy trạng thái hiện tại của timer"""
        return self.timer_core.get_state()

    def set_time(self, seconds):
        """Thiết lập thời gian timer (để mở rộng tính năng)"""
        self.timer_core.time_elapsed = seconds
        self.timer_core.on_timer_update(self.timer_core.format_time(seconds))

    def add_time(self, seconds):
        """Thêm thời gian vào timer (để mở rộng tính năng)"""
        self.timer_core.time_elapsed += seconds
        self.timer_core.on_timer_update(self.timer_core.format_time(self.timer_core.time_elapsed))

    def toggle_sound(self):
        """Bật/tắt âm thanh"""
        return self.sound_manager.toggle_sound()

    def set_volume(self, volume):
        """Điều chỉnh âm lượng (0.0 - 1.0)"""
        self.sound_manager.set_volume(volume)
