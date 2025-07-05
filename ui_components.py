"""
UI Components Module - Quản lý giao diện người dùng
"""

import tkinter as tk
from tkinter import font as tkfont
from task_ui import TaskUI

class FliqloUI:
    def __init__(self, root):
        self.root = root
        self._setup_window()
        self._create_widgets()
        
        # Callbacks cho các sự kiện
        self.on_start = None
        self.on_toggle = None
        self.on_reset = None
        self.on_sessions_changed = None
        self.on_auto_continue_changed = None
        self.on_reset_sessions = None
        
        # Task callbacks
        self.on_add_task = None
        self.on_complete_task = None
        self.on_delete_task = None
        self.on_edit_task = None
        self.on_clear_completed = None
        
        # Sound manager callback
        self.play_sound = None

    def _setup_window(self):
        """Thiết lập cửa sổ chính"""
        self.root.title("Fliqlo Timer - Session & Task Manager")
        self.root.configure(bg='black')
        self.root.geometry("900x650")

    def _create_widgets(self):
        """Tạo các widget UI"""
        # Font lớn, đậm, dễ đọc kiểu Fliqlo
        self.clock_font = tkfont.Font(family="Courier New", size=72, weight="bold")
        self.break_font = tkfont.Font(family="Courier New", size=36, weight="bold")
        self.info_font = tkfont.Font(family="Courier New", size=16, weight="bold")

        # Session info frame
        self.session_frame = tk.Frame(self.root, bg='black')
        self.session_frame.pack(pady=10)

        # Session counter
        self.session_label = tk.Label(
            self.session_frame,
            text="Session: 0/8",
            font=self.info_font,
            fg="yellow",
            bg="black"
        )
        self.session_label.pack(side=tk.LEFT, padx=20)

        # Progress indicator
        self.progress_label = tk.Label(
            self.session_frame,
            text="Progress: 0%",
            font=self.info_font,
            fg="orange",
            bg="black"
        )
        self.progress_label.pack(side=tk.LEFT, padx=20)

        # Main timer label
        self.timer_label = tk.Label(
            self.root, 
            text="00:00:00", 
            font=self.clock_font, 
            fg="white", 
            bg="black"
        )
        self.timer_label.pack(pady=40)

        # Break timer label (màu xanh)
        self.break_label = tk.Label(
            self.root, 
            text="", 
            font=self.break_font, 
            fg="cyan", 
            bg="black"
        )
        self.break_label.pack(pady=10)

        # Settings frame
        self._create_settings()

        # Button frame
        self._create_buttons()

        # Task management frame
        self.task_ui = TaskUI(self.root)

    def _create_buttons(self):
        """Tạo các nút điều khiển"""
        btn_frame = tk.Frame(self.root, bg='black')
        btn_frame.pack()

        self.start_btn = tk.Button(
            btn_frame, 
            text="Start", 
            width=10, 
            command=self._on_start_clicked
        )
        self.start_btn.grid(row=0, column=0, padx=5)

        self.toggle_btn = tk.Button(
            btn_frame, 
            text="Pause", 
            width=10, 
            command=self._on_toggle_clicked
        )
        self.toggle_btn.grid(row=0, column=1, padx=5)

        self.reset_btn = tk.Button(
            btn_frame, 
            text="Reset", 
            width=10, 
            command=self._on_reset_clicked
        )
        self.reset_btn.grid(row=0, column=2, padx=5)

    def _create_settings(self):
        """Tạo phần cài đặt session"""
        settings_frame = tk.Frame(self.root, bg='black')
        settings_frame.pack(pady=10)

        # Target sessions setting
        tk.Label(settings_frame, text="Target Sessions:", fg="white", bg="black").grid(row=0, column=0, padx=5)
        self.sessions_var = tk.StringVar(value="8")
        self.sessions_spinbox = tk.Spinbox(
            settings_frame,
            from_=1, to=20,
            textvariable=self.sessions_var,
            width=5,
            command=self._on_sessions_changed
        )
        self.sessions_spinbox.grid(row=0, column=1, padx=5)

        # Auto continue setting
        self.auto_continue_var = tk.BooleanVar(value=True)
        self.auto_continue_cb = tk.Checkbutton(
            settings_frame,
            text="Auto Continue",
            variable=self.auto_continue_var,
            fg="white",
            bg="black",
            selectcolor="black",
            command=self._on_auto_continue_changed
        )
        self.auto_continue_cb.grid(row=0, column=2, padx=10)

        # Reset sessions button
        self.reset_sessions_btn = tk.Button(
            settings_frame,
            text="Reset Sessions",
            width=12,
            command=self._on_reset_sessions_clicked
        )
        self.reset_sessions_btn.grid(row=0, column=3, padx=5)

    def _on_start_clicked(self):
        """Xử lý sự kiện click nút Start"""
        if self.play_sound:
            self.play_sound('start')
        if self.on_start:
            self.on_start()

    def _on_toggle_clicked(self):
        """Xử lý sự kiện click nút Pause/Resume"""
        if self.play_sound:
            self.play_sound('pause')
        if self.on_toggle:
            self.on_toggle()

    def _on_reset_clicked(self):
        """Xử lý sự kiện click nút Reset"""
        if self.play_sound:
            self.play_sound('reset')
        if self.on_reset:
            self.on_reset()

    def _on_sessions_changed(self):
        """Xử lý sự kiện thay đổi target sessions"""
        if self.on_sessions_changed:
            try:
                sessions = int(self.sessions_var.get())
                self.on_sessions_changed(sessions)
            except ValueError:
                pass

    def _on_auto_continue_changed(self):
        """Xử lý sự kiện thay đổi auto continue"""
        if self.on_auto_continue_changed:
            self.on_auto_continue_changed(self.auto_continue_var.get())

    def _on_reset_sessions_clicked(self):
        """Xử lý sự kiện reset sessions"""
        if self.on_reset_sessions:
            self.on_reset_sessions()

    def update_timer_display(self, time_text):
        """Cập nhật hiển thị timer chính"""
        self.timer_label.config(text=time_text)

    def update_break_display(self, break_text):
        """Cập nhật hiển thị break timer"""
        self.break_label.config(text=break_text)

    def update_button_state(self, state):
        """Cập nhật trạng thái các nút"""
        if state == "running":
            self.toggle_btn.config(text="Pause")
        elif state == "paused":
            self.toggle_btn.config(text="Resume")
        elif state == "reset":
            self.toggle_btn.config(text="Pause")
        elif state == "session_complete":
            self.toggle_btn.config(text="Resume")

    def update_session_display(self, current, target):
        """Cập nhật hiển thị session"""
        self.session_label.config(text=f"Session: {current}/{target}")

    def update_progress_display(self, progress):
        """Cập nhật hiển thị tiến độ"""
        self.progress_label.config(text=f"Progress: {progress:.1f}%")

    def show_session_complete_message(self, session, target):
        """Hiển thị thông báo hoàn thành session"""
        import tkinter.messagebox as msgbox
        if session >= target:
            msgbox.showinfo("Congratulations!", f"🎉 You completed all {target} sessions today!\nGreat work!")
        else:
            msgbox.showinfo("Session Complete", f"✅ Session {session} completed!\n{target - session} sessions remaining.")

    def setup_task_callbacks(self):
        """Thiết lập callbacks cho task UI"""
        self.task_ui.on_add_task = self.on_add_task
        self.task_ui.on_complete_task = self.on_complete_task
        self.task_ui.on_delete_task = self.on_delete_task
        self.task_ui.on_edit_task = self.on_edit_task
        self.task_ui.on_clear_completed = self.on_clear_completed

    def update_task_list(self, tasks):
        """Cập nhật danh sách tasks"""
        self.task_ui.update_task_list(tasks)

    def update_completed_task_list(self, completed_tasks):
        """Cập nhật danh sách completed tasks"""
        self.task_ui.update_completed_list(completed_tasks)

    def update_task_summary(self, summary):
        """Cập nhật task summary"""
        self.task_ui.update_summary(summary)

    def show_task_complete_notification(self, task):
        """Hiển thị thông báo hoàn thành task"""
        self.task_ui.show_task_complete_notification(task)

    def get_widgets(self):
        """Trả về dictionary chứa các widget chính"""
        return {
            'timer_label': self.timer_label,
            'break_label': self.break_label,
            'session_label': self.session_label,
            'progress_label': self.progress_label,
            'start_btn': self.start_btn,
            'toggle_btn': self.toggle_btn,
            'reset_btn': self.reset_btn,
            'sessions_spinbox': self.sessions_spinbox,
            'auto_continue_cb': self.auto_continue_cb,
            'task_ui': self.task_ui
        }
