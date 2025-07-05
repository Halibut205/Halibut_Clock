"""
Timer Core Module - Quản lý logic đồng hồ chính và break timer
"""

class TimerCore:
    def __init__(self):
        self.running = False
        self.time_elapsed = 0  # tính bằng giây
        self.break_running = False
        self.break_time = 0  # thời gian nghỉ
        
        # Session management
        self.current_session = 0
        self.target_sessions = 8  # Default 8 sessions per day
        self.session_duration = 3600  # 1 hour = 3600 seconds
        self.auto_continue = True  # Tự động tiếp tục sau mỗi session
        self.session_completed = False
        
        # Callbacks để update UI
        self.on_timer_update = None
        self.on_break_update = None
        self.on_state_change = None
        self.on_session_update = None
        self.on_session_complete = None

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
            self.session_completed = False
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
        self.session_completed = False
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
            
            # Kiểm tra nếu hoàn thành 1 session (1 giờ)
            if self.time_elapsed >= self.session_duration and not self.session_completed:
                self._complete_session()
            
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
            'formatted_break': self.format_time(self.break_time),
            'current_session': self.current_session,
            'target_sessions': self.target_sessions,
            'session_progress': min(self.time_elapsed / self.session_duration * 100, 100),
            'auto_continue': self.auto_continue
        }

    def _complete_session(self):
        """Xử lý khi hoàn thành 1 session"""
        self.session_completed = True
        self.current_session += 1
        
        if self.on_session_complete:
            self.on_session_complete(self.current_session, self.target_sessions)
        
        if self.on_session_update:
            self.on_session_update(self.current_session, self.target_sessions)
        
        # Kiểm tra xem có tiếp tục tự động không
        if self.auto_continue and self.current_session < self.target_sessions:
            # Tiếp tục session mới
            self.time_elapsed = 0
            self.session_completed = False
        else:
            # Dừng và chuyển sang break
            self.running = False
            self.break_running = True
            if self.on_state_change:
                self.on_state_change("session_complete")

    def set_target_sessions(self, sessions):
        """Thiết lập số session mục tiêu"""
        self.target_sessions = max(1, sessions)
        if self.on_session_update:
            self.on_session_update(self.current_session, self.target_sessions)

    def set_auto_continue(self, auto_continue):
        """Thiết lập có tự động tiếp tục sau mỗi session không"""
        self.auto_continue = auto_continue

    def reset_sessions(self):
        """Reset session về 0"""
        self.current_session = 0
        if self.on_session_update:
            self.on_session_update(self.current_session, self.target_sessions)

    def get_session_progress(self):
        """Lấy tiến độ của session hiện tại (0-100%)"""
        return min(self.time_elapsed / self.session_duration * 100, 100)

    def get_remaining_time(self):
        """Lấy thời gian còn lại của session hiện tại"""
        remaining = self.session_duration - self.time_elapsed
        return max(0, remaining)
