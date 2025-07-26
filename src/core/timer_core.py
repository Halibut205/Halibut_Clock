"""
Timer Core Module - Dual Clock System (Main + Break)
Handles the core timing logic with session management and unlimited sessions support.
"""

from typing import Optional, Callable


class TimerCore:
    """
    Core timer logic with dual clock system and unlimited sessions.
    
    Manages the main timing functionality including session tracking,
    dual clock system (main/break), and unlimited session support.
    """
    
    def __init__(self):
        # Dual clock system
        self.main_running = False
        self.break_running = False
        self.main_time = 0  # Main timer elapsed time (seconds)
        self.break_time = 0  # Break timer elapsed time (seconds)
        self.break_session_time = 0  # Hidden timer cho break session hiện tại
        
        # Session management
        self.current_session = 0
        self.target_sessions = 8
        self.session_duration = 3600  # 1 hour default
        self.break_duration = 300  # 5 minutes default
        self.auto_continue = False
        self.last_session_check = 0  # Track last session completion time
        
        # State management
        self.session_completed = False
        self.all_sessions_completed = False
        self.waiting_for_user_choice = False
        
        # UI callback functions
        self.on_main_timer_update: Optional[Callable] = None
        self.on_break_timer_update: Optional[Callable] = None
        self.on_state_change: Optional[Callable] = None
        self.on_session_update: Optional[Callable] = None
        self.on_session_complete: Optional[Callable] = None
        self.on_all_sessions_complete: Optional[Callable] = None
        self.on_choice_required: Optional[Callable] = None

    def format_time(self, seconds):
        """Format thời gian thành HH:MM:SS"""
        hrs = seconds // 3600
        mins = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hrs:02}:{mins:02}:{secs:02}"

    def start_main_timer(self):
        """Bắt đầu main timer, freeze break timer và reset hidden timer"""
        self.main_running = True
        self.break_running = False
        self.break_session_time = 0  # Reset hidden timer về 0
        self.waiting_for_user_choice = False
        if self.on_state_change:
            self.on_state_change("main_running")

    def start_break_timer(self):
        """Bắt đầu break timer, freeze main timer và reset hidden timer"""
        self.main_running = False
        self.break_running = True
        self.break_session_time = 0  # Reset hidden timer về 0
        self.waiting_for_user_choice = False
        if self.on_state_change:
            self.on_state_change("break_running")

    def pause_main_start_break(self):
        """Pause main timer và start break timer"""
        self.main_running = False
        self.break_running = True
        self.break_session_time = 0  # Reset hidden timer về 0
        if self.on_state_change:
            self.on_state_change("break_running")

    def pause_break_start_main(self):
        """Pause break timer và resume main timer"""
        self.break_running = False
        self.main_running = True
        if self.on_state_change:
            self.on_state_change("main_running")

    def freeze_all(self):
        """Freeze cả hai đồng hồ"""
        self.main_running = False
        self.break_running = False
        if self.on_state_change:
            self.on_state_change("all_frozen")

    def reset_timers(self):
        """Reset cả hai timer về 0"""
        self.main_running = False
        self.break_running = False
        self.main_time = 0
        self.break_time = 0
        self.break_session_time = 0  # Reset hidden timer
        self.current_session = 0
        self.last_session_check = 0  # Reset session check
        self.session_completed = False
        self.all_sessions_completed = False
        self.waiting_for_user_choice = False
        if self.on_state_change:
            self.on_state_change("reset")

    def tick(self):
        """Update timers mỗi giây"""
        # Update main timer
        if self.main_running:
            self.main_time += 1
            if self.on_main_timer_update:
                self.on_main_timer_update(self.format_time(self.main_time))
            
            # Check session completion - khi đạt session_duration
            session_boundary = ((self.current_session + 1) * self.session_duration)
            
            if self.main_time >= session_boundary and self.main_time > self.last_session_check:
                self.last_session_check = self.main_time
                self._handle_session_complete()
        
        # Update break timer
        if self.break_running:
            self.break_time += 1
            self.break_session_time += 1  # Tăng hidden timer
            if self.on_break_timer_update:
                self.on_break_timer_update(self.format_time(self.break_time), self.break_session_time)

    def _handle_session_complete(self):
        """Xử lý khi hoàn thành một session"""
        print(f"🎯 Session {self.current_session + 1} hoàn thành!")
        self.current_session += 1
        self.session_completed = True
        
        # Freeze cả hai đồng hồ khi session complete
        self.freeze_all()
        self.waiting_for_user_choice = True
        
        # Cập nhật session display trước
        if self.on_session_update:
            self.on_session_update(self.current_session, self.target_sessions)
        
        # Play completion sound trước
        if self.on_session_complete:
            self.on_session_complete()
        
        # Check if reached target sessions
        if self.current_session >= self.target_sessions:
            self.all_sessions_completed = True
            # Chỉ hiển thị all sessions complete message nếu auto_continue = False
            if not self.auto_continue and self.on_all_sessions_complete:
                self.on_all_sessions_complete()
        
        # Luôn hiển thị choice dialog (trừ khi auto_continue = True và chưa đạt target)
        should_show_choice = True
        if self.auto_continue and self.current_session < self.target_sessions:
            # Auto continue và chưa đạt target -> không hiển thị choice, tự động tiếp tục
            should_show_choice = False
            self.waiting_for_user_choice = False  # Reset trước khi auto continue
            print("🤖 Auto continue enabled - continuing next session...")
            self.choose_continue_session()
        
        if should_show_choice:
            print("🔔 Chuẩn bị gọi on_choice_required...")
            if self.on_choice_required:
                print("🔔 Đang gọi on_choice_required!")
                self.on_choice_required()
            else:
                print("❌ on_choice_required is None!")

    def choose_continue_session(self):
        """User chọn tiếp tục session tiếp theo"""
        print("✅ Continue session selected")
        self.session_completed = False
        self.waiting_for_user_choice = False
        # Reset all_sessions_completed nếu user chọn tiếp tục beyond target
        if self.all_sessions_completed:
            self.all_sessions_completed = False
        self.start_main_timer()

    def choose_take_break(self):
        """User chọn nghỉ break"""
        print("☕ Take break selected")
        self.session_completed = False
        self.waiting_for_user_choice = False
        # Reset all_sessions_completed nếu user chọn tiếp tục beyond target
        if self.all_sessions_completed:
            self.all_sessions_completed = False
        self.start_break_timer()

    # Getters for UI
    def get_main_time_text(self):
        return self.format_time(self.main_time)
    
    def get_break_time_text(self):
        return self.format_time(self.break_time)
    
    def is_main_running(self):
        return self.main_running
    
    def is_break_running(self):
        return self.break_running
    
    def is_waiting_for_choice(self):
        return self.waiting_for_user_choice

    # Session management
    def set_target_sessions(self, sessions):
        self.target_sessions = sessions

    def set_session_duration(self, duration):
        self.session_duration = duration

    def set_auto_continue(self, auto_continue):
        self.auto_continue = auto_continue

    def force_session_complete(self):
        """Trigger session completion manually for testing"""
        self._handle_session_complete()

    def set_test_mode(self):
        """Set short session duration for testing (10 seconds)"""
        self.session_duration = 10
        print(f"🧪 Test mode: Session duration = {self.session_duration} seconds")

    def reset_sessions(self):
        self.current_session = 0
        if self.on_session_update:
            self.on_session_update(self.current_session, self.target_sessions)

    def get_session_progress(self):
        """Lấy tiến độ của session hiện tại (0-100%)"""
        if self.session_duration <= 0:
            return 0
        
        # Nếu đang trong trạng thái session complete, hiển thị 100%
        if self.session_completed or self.waiting_for_user_choice:
            return 100.0
            
        # Tính progress của session hiện tại
        current_session_time = self.main_time % self.session_duration
        return min(current_session_time / self.session_duration * 100, 100)

    def get_state(self):
        """Lấy trạng thái hiện tại của timer"""
        return {
            'main_running': self.main_running,
            'break_running': self.break_running,
            'main_time': self.main_time,
            'break_time': self.break_time,
            'formatted_main_time': self.format_time(self.main_time),
            'formatted_break_time': self.format_time(self.break_time),
            'current_session': self.current_session,
            'target_sessions': self.target_sessions,
            'session_progress': self.get_session_progress(),
            'waiting_for_choice': self.waiting_for_user_choice,
            'all_sessions_completed': self.all_sessions_completed
        }

