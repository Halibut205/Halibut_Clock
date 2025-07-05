"""
Timer Core Module - Quản lý logic đồng hồ chính và break timer
"""

class TimerCore:
    def __init__(self):
        self.running = False
        self.time_elapsed = 0  # tính bằng giây
        self.break_running = False
        self.break_time = 0  # thời gian nghỉ
        
        # Callbacks để update UI
        self.on_timer_update = None
        self.on_break_update = None
        self.on_state_change = None

    def format_time(self, seconds):
        """Format thời gian thành HH:MM:SS"""
        hrs = seconds // 3600
        mins = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hrs:02}:{mins:02}:{secs:02}"

    def start_timer(self):
        """Bắt đầu timer chính"""
        if not self.running:
            self.running = True
            self.time_elapsed = 0
            self.break_running = False  # Dừng break timer nếu có
            self.break_time = 0  # Reset break time khi start
            if self.on_state_change:
                self.on_state_change("running")
            if self.on_break_update:
                self.on_break_update("")  # Xóa hiển thị break timer

    def pause_timer(self):
        """Tạm dừng timer chính và bắt đầu break timer"""
        if self.running:
            self.running = False
            # Bắt đầu break timer (không reset nếu đã có thời gian từ trước)
            if not self.break_running:
                self.break_running = True
            if self.on_state_change:
                self.on_state_change("paused")

    def resume_timer(self):
        """Tiếp tục timer chính và dừng break timer"""
        if not self.running:
            self.running = True
            self.break_running = False  # Freeze break timer
            if self.on_state_change:
                self.on_state_change("running")

    def reset_timer(self):
        """Reset tất cả timer về 0"""
        self.running = False
        self.break_running = False
        self.time_elapsed = 0
        self.break_time = 0
        if self.on_state_change:
            self.on_state_change("reset")
        if self.on_timer_update:
            self.on_timer_update("00:00:00")
        if self.on_break_update:
            self.on_break_update("")

    def tick(self):
        """Cập nhật timer mỗi giây"""
        updated = False
        
        if self.running:
            self.time_elapsed += 1
            if self.on_timer_update:
                self.on_timer_update(self.format_time(self.time_elapsed))
            updated = True
            
        if self.break_running:
            self.break_time += 1
            if self.on_break_update:
                self.on_break_update(f"Break: {self.format_time(self.break_time)}")
            updated = True
            
        return updated

    def get_state(self):
        """Lấy trạng thái hiện tại của timer"""
        return {
            'running': self.running,
            'break_running': self.break_running,
            'time_elapsed': self.time_elapsed,
            'break_time': self.break_time,
            'formatted_time': self.format_time(self.time_elapsed),
            'formatted_break': self.format_time(self.break_time)
        }
