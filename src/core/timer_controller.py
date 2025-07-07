"""
Timer Controller Module - Điều phối giữa UI và Timer Core
"""

import tkinter as tk
from datetime import datetime
from .timer_core import TimerCore
from ..ui.ui_components import FliqloUI
from ..managers.sound_manager import SoundManager
from ..managers.task_manager import TaskManager

class TimerController:
    def __init__(self, root):
        self.root = root
        
        # Khởi tạo core logic, UI, sound và task manager
        self.timer_core = TimerCore()
        self.ui = FliqloUI(root)
        self.sound_manager = SoundManager()
        self.task_manager = TaskManager()
        
        # Kết nối callbacks
        self._setup_callbacks()
        
        # Load và hiển thị tasks
        self._refresh_task_display()
        
        # Bắt đầu update loop
        self._update_loop()

    def _setup_callbacks(self):
        """Thiết lập callbacks giữa UI và Core"""
        # UI callbacks
        self.ui.on_start = self._handle_start
        self.ui.on_toggle = self._handle_toggle
        self.ui.on_reset = self._handle_reset
        self.ui.on_sessions_changed = self._handle_sessions_changed
        self.ui.on_auto_continue_changed = self._handle_auto_continue_changed
        self.ui.on_reset_sessions = self._handle_reset_sessions
        self.ui.on_session_duration_changed = self._handle_session_duration_changed  # New callback
        self.ui.on_help_clicked = self._handle_help_clicked  # Help callback
        
        # Task callbacks
        self.ui.on_add_task = self._handle_add_task
        self.ui.on_complete_task = self._handle_complete_task
        self.ui.on_delete_task = self._handle_delete_task
        self.ui.on_edit_task = self._handle_edit_task
        self.ui.on_reactivate_task = self._handle_reactivate_task  # New callback
        self.ui.on_clear_completed = self._handle_clear_completed
        
        # Setup task UI callbacks
        self.ui.setup_task_callbacks()
        
        # Connect sound to UI buttons
        self.ui.play_sound = self.sound_manager.play_button_click
        
        # Core callbacks - Updated for dual clock system
        self.timer_core.on_main_timer_update = self.ui.update_main_timer_display
        self.timer_core.on_break_timer_update = self.ui.update_break_timer_display
        self.timer_core.on_state_change = self.ui.update_button_state
        self.timer_core.on_session_update = self._update_session_display
        self.timer_core.on_session_complete = self._handle_session_complete
        self.timer_core.on_all_sessions_complete = self._handle_all_sessions_complete
        self.timer_core.on_choice_required = self._show_user_choice_dialog
        
        # Task manager callbacks
        self.task_manager.on_task_added = self._on_task_added
        self.task_manager.on_task_completed = self._on_task_completed
        self.task_manager.on_tasks_updated = self._refresh_task_display

    def _handle_start(self):
        """Xử lý sự kiện Start - Bắt đầu main timer"""
        self.timer_core.start_main_timer()
        # Bắt đầu background music khi start timer
        self.sound_manager.start_background_music()

    def _handle_toggle(self):
        """Xử lý sự kiện Toggle - Chuyển đổi giữa main và break timer"""
        if self.timer_core.is_main_running():
            # Main đang chạy -> pause main, start break
            self.timer_core.pause_main_start_break()
            # Pause background music khi chuyển sang break
            self.sound_manager.pause_background_music()
        elif self.timer_core.is_break_running():
            # Break đang chạy -> pause break, start main
            self.timer_core.pause_break_start_main()
            # Resume background music khi quay lại main
            self.sound_manager.resume_background_music()
        else:
            # Cả hai đều freeze -> start main timer
            self.timer_core.start_main_timer()
            self.sound_manager.start_background_music()

    def _handle_reset(self):
        """Xử lý sự kiện Reset - Reset cả hai timer"""
        self.timer_core.reset_timers()
        # Dừng background music khi reset
        self.sound_manager.stop_background_music()

    def _handle_sessions_changed(self, sessions):
        """Xử lý sự kiện thay đổi target sessions"""
        self.timer_core.set_target_sessions(sessions)

    def _handle_auto_continue_changed(self, auto_continue):
        """Xử lý sự kiện thay đổi auto continue"""
        self.timer_core.set_auto_continue(auto_continue)

    def _handle_reset_sessions(self):
        """Xử lý sự kiện reset sessions"""
        self.timer_core.reset_sessions()

    def _handle_add_task(self, task_text):
        """Xử lý sự kiện thêm task"""
        current_session = self.timer_core.current_session + 1  # Next session
        self.task_manager.add_task(task_text, current_session)

    def _handle_complete_task(self, task_index):
        """Xử lý sự kiện hoàn thành task"""
        tasks = self.task_manager.get_all_active_tasks()
        if 0 <= task_index < len(tasks):
            task = tasks[task_index]
            self.task_manager.complete_task(task['id'])
            self.sound_manager.play_button_click()

    def _handle_delete_task(self, task_index):
        """Xử lý sự kiện xóa task"""
        tasks = self.task_manager.get_all_active_tasks()
        if 0 <= task_index < len(tasks):
            task = tasks[task_index]
            self.task_manager.delete_task(task['id'])

    def _handle_edit_task(self, task_index, new_text):
        """Xử lý sự kiện chỉnh sửa task"""
        tasks = self.task_manager.get_all_active_tasks()
        if 0 <= task_index < len(tasks):
            task = tasks[task_index]
            self.task_manager.edit_task(task['id'], new_text)

    def _handle_reactivate_task(self, task_index):
        """Xử lý sự kiện reactivate completed task"""
        completed_tasks = self.task_manager.get_completed_tasks()
        if 0 <= task_index < len(completed_tasks):
            task = completed_tasks[task_index]
            self.task_manager.reactivate_task(task['id'])
            self.sound_manager.play_button_click()

    def _handle_clear_completed(self):
        """Xử lý sự kiện xóa tất cả completed tasks"""
        self.task_manager.clear_completed_tasks()

    def _handle_session_duration_changed(self, duration_seconds, duration_label):
        """Xử lý sự kiện thay đổi session duration"""
        self.timer_core.set_session_duration(duration_seconds)
        print(f"Session duration changed to: {duration_label} ({duration_seconds} seconds)")

    def _handle_help_clicked(self):
        """Xử lý sự kiện click Help - show welcome screen"""
        from ..ui.welcome_screen import show_welcome_screen
        
        # Tạm ẩn main window
        self.root.withdraw()
        
        def on_welcome_close():
            # Hiện lại main window
            self.root.deiconify()
        
        # Show welcome screen
        show_welcome_screen(on_welcome_close)

    def _handle_session_complete(self):
        """Xử lý khi hoàn thành một session"""
        # Play completion sound (rang.mp3)
        self.sound_manager.play_completion_sound()
        
        # Pause background music
        self.sound_manager.pause_background_music()
        
        # Show completion message
        self.ui.show_session_complete_message()
    
    def _handle_all_sessions_complete(self):
        """Xử lý khi hoàn thành tất cả sessions"""
        # Play completion sound
        self.sound_manager.play_completion_sound()
        
        # Stop background music
        self.sound_manager.stop_background_music()
        
        # Show congratulations message
        self.ui.show_all_sessions_complete_message()
    
    def _show_user_choice_dialog(self):
        """Hiển thị dialog cho user chọn tiếp tục hay nghỉ"""
        import tkinter.messagebox as messagebox
        
        choice = messagebox.askyesno(
            "Session Complete! 🎉",
            f"Completed session {self.timer_core.current_session}/{self.timer_core.target_sessions}!\n\n"
            "What would you like to do next?\n\n"
            "YES = Continue next session\n"
            "NO = Take a break",
            icon='question'
        )
        
        if choice:
            # User chose to continue
            self.timer_core.choose_continue_session()
            self.sound_manager.start_background_music()
        else:
            # User chose to take break
            self.timer_core.choose_take_break()
            # No background music during break

    def _on_task_added(self, task):
        """Callback khi task được thêm"""
        print(f"✅ Task added: {task['text']}")

    def _on_task_completed(self, task):
        """Callback khi task được hoàn thành"""
        self.ui.show_task_complete_notification(task)

    def _refresh_task_display(self):
        """Refresh hiển thị tasks"""
        tasks = self.task_manager.get_all_active_tasks()
        completed_tasks = self.task_manager.get_completed_tasks()
        summary = self.task_manager.get_tasks_summary()
        
        self.ui.update_task_list(tasks)
        self.ui.update_completed_task_list(completed_tasks)
        self.ui.update_task_summary(summary)

    def _update_loop(self):
        """Vòng lặp cập nhật timer mỗi giây"""
        self.timer_core.tick()
        
        # Cập nhật progress bar
        progress = self.timer_core.get_session_progress()
        self.ui.update_progress_display(progress)
        
        # Lặp lại sau 1 giây
        self.root.after(1000, self._update_loop)

    def get_timer_state(self):
        """Lấy trạng thái hiện tại của timer"""
        return self.timer_core.get_state()

    def set_time(self, seconds):
        """Thiết lập thời gian timer (để mở rộng tính năng)"""
        self.timer_core.main_time = seconds
        if self.timer_core.on_main_timer_update:
            self.timer_core.on_main_timer_update(self.timer_core.format_time(seconds))

    def add_time(self, seconds):
        """Thêm thời gian vào timer (để mở rộng tính năng)"""
        self.timer_core.main_time += seconds
        if self.timer_core.on_main_timer_update:
            self.timer_core.on_main_timer_update(self.timer_core.format_time(self.timer_core.main_time))

    def toggle_sound(self):
        """Bật/tắt âm thanh"""
        return self.sound_manager.toggle_sound()

    def set_volume(self, volume):
        """Điều chỉnh âm lượng (0.0 - 1.0)"""
        self.sound_manager.set_volume(volume)

    def get_task_summary(self):
        """Lấy tóm tắt tasks"""
        return self.task_manager.get_tasks_summary()

    def export_tasks(self, filename=None):
        """Export tasks ra file"""
        if not filename:
            filename = f"tasks_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            import shutil
            shutil.copy(self.task_manager.data_file, filename)
            return filename
        except Exception as e:
            print(f"❌ Could not export tasks: {e}")
            return None

    def import_tasks(self, filename):
        """Import tasks từ file"""
        try:
            import shutil
            shutil.copy(filename, self.task_manager.data_file)
            self.task_manager.load_tasks()
            self._refresh_task_display()
            return True
        except Exception as e:
            print(f"❌ Could not import tasks: {e}")
            return False

    def _update_session_display(self, current, target):
        """Update session display với current và target sessions"""
        self.ui.update_session_display(current, target)
