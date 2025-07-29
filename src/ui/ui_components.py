"""
UI Components Module - Main user interface components for the Study Timer
"""

import tkinter as tk
from tkinter import font as tkfont
from typing import Dict

from .task_ui import TaskUI

# Session duration options mapping
SESSION_DURATION_OPTIONS: Dict[str, int] = {
    "🧪 1 min (DEBUG)": 1 * 60,    # 60 seconds (debug only)
    "15 min": 15 * 60,      # 900 seconds
    "25 min": 25 * 60,      # 1500 seconds (Pomodoro)
    "30 min": 30 * 60,      # 1800 seconds
    "45 min": 45 * 60,      # 2700 seconds
    "1 hour": 60 * 60,      # 3600 seconds (default)
    "1.5 hours": 90 * 60,   # 5400 seconds
    "2 hours": 120 * 60     # 7200 seconds
}


class StudyTimerUI:
    """Main UI class for the Study Timer interface"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self._setup_window()
        self._create_widgets()
        
        # Event callbacks
        self.on_start = None
        self.on_toggle = None
        self.on_reset = None
        self.on_sessions_changed = None
        self.on_auto_continue_changed = None
        self.on_reset_sessions = None
        self.on_session_duration_changed = None
        self.on_help_clicked = None  # Help callback
        self.on_stats_clicked = None  # Stats window callback
        self.on_mute_clicked = None  # Mute/unmute background music callback
        
        # Task callbacks
        self.on_add_task = None
        self.on_complete_task = None
        self.on_delete_task = None
        self.on_edit_task = None
        self.on_reactivate_task = None
        self.on_move_task_up = None
        self.on_move_task_down = None
        
        # Sound callback (deprecated - use specific sound callbacks)
        self.play_sound = None
        
        # Sound callbacks for different button types
        self.play_main_button_sound = None      # For START, PAUSE/RESUME
        self.play_secondary_button_sound = None # For RESET, Help, Mute
        self.play_stats_button_sound = None     # For Daily Stats
        self.on_clear_completed = None
        
        # Choice overlay callbacks
        self.on_continue_session = None
        self.on_take_break = None
        
        # Sound manager callback
        self.play_sound = None
        
        # Choice overlay
        self.choice_overlay = None

    def _setup_window(self):
        """Thiết lập cửa sổ chính"""
        self.root.title("Study Timer")
        self.root.configure(bg='black')
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Bind keyboard shortcut for debug toggle (Ctrl+D)
        self.root.bind('<Control-d>', lambda e: self._on_debug_toggle_clicked())
        self.root.bind('<Control-D>', lambda e: self._on_debug_toggle_clicked())

    def _create_widgets(self):
        """Tạo các widget UI"""
        # Font settings
        self.clock_font = tkfont.Font(family="Courier New", size=36, weight="bold")
        self.break_font = tkfont.Font(family="Courier New", size=18, weight="bold")
        self.info_font = tkfont.Font(family="Courier New", size=12, weight="bold")

        # Session info frame
        self.session_frame = tk.Frame(self.root, bg='black')
        self.session_frame.pack(pady=5)

        # Session counter
        self.session_label = tk.Label(
            self.session_frame,
            text="Session: 0/8",
            font=self.info_font,
            fg="yellow",
            bg="black"
        )
        self.session_label.pack(side=tk.LEFT, padx=10)

        # Progress indicator
        self.progress_label = tk.Label(
            self.session_frame,
            text="Progress: 0%",
            font=self.info_font,
            fg="orange",
            bg="black"
        )
        self.progress_label.pack(side=tk.RIGHT, padx=10)

        # Main timer label
        self.main_timer_label = tk.Label(
            self.root, 
            text="00:00:00", 
            font=self.clock_font, 
            fg="white", 
            bg="black"
        )
        self.main_timer_label.pack(pady=5)

        # Break timer section with hidden timer
        break_frame = tk.Frame(self.root, bg='black')
        break_frame.pack(pady=5)
        
        # Break timer label - compact (main)
        self.break_timer_label = tk.Label(
            break_frame, 
            text="Break: 00:00:00", 
            font=self.break_font, 
            fg="cyan", 
            bg="black"
        )
        self.break_timer_label.pack(side="left")
        
        # Hidden timer label - smaller, on the right
        self.hidden_timer_label = tk.Label(
            break_frame,
            text="00:00",
            font=tkfont.Font(family="Arial", size=10),
            fg="gray",
            bg="black"
        )
        self.hidden_timer_label.pack(side="left", padx=(10, 0))

        # Help and stats buttons frame
        help_frame = tk.Frame(self.root, bg='black')
        help_frame.pack(pady=5)
        
        help_btn_top = tk.Button(
            help_frame,
            text="❓ Trợ giúp / Help",
            font=tkfont.Font(family="Arial", size=10, weight="bold"),
            width=18,
            height=1,
            bg="purple",
            fg="white",
            command=self._on_help_clicked
        )
        help_btn_top.pack(side="left", padx=(0, 5))
        
        # Daily stats button
        stats_btn = tk.Button(
            help_frame,
            text="📊 Daily Stats",
            font=tkfont.Font(family="Arial", size=10, weight="bold"),
            width=18,
            height=1,
            bg="#2c3e50",
            fg="white",
            command=self._on_stats_clicked
        )
        stats_btn.pack(side="left", padx=5)

        # Mute button for background music
        self.mute_btn = tk.Button(
            help_frame,
            text="🔊 Sound",
            font=tkfont.Font(family="Arial", size=10, weight="bold"),
            width=12,
            height=1,
            bg="#27ae60",
            fg="white",
            command=self._on_mute_clicked
        )
        self.mute_btn.pack(side="left", padx=5)

        # Main control buttons
        self._create_main_buttons()

        # Settings frame
        self._create_settings()

        # Task management frame
        self.task_ui = TaskUI(self.root)

    def _create_main_buttons(self):
        """Tạo các nút điều khiển chính"""
        btn_frame = tk.Frame(self.root, bg='black')
        btn_frame.pack(pady=10)

        # Control buttons with large font
        btn_font = tkfont.Font(family="Arial", size=14, weight="bold")
        
        self.start_btn = tk.Button(
            btn_frame, 
            text="▶ START", 
            font=btn_font,
            width=12, 
            height=2,
            bg="green",
            fg="white",
            command=self._on_start_clicked
        )
        self.start_btn.grid(row=0, column=0, padx=8, pady=5)

        self.toggle_btn = tk.Button(
            btn_frame, 
            text="⏸ PAUSE", 
            font=btn_font,
            width=12,
            height=2,
            bg="orange",
            fg="white", 
            command=self._on_toggle_clicked
        )
        self.toggle_btn.grid(row=0, column=1, padx=8, pady=5)

        self.reset_btn = tk.Button(
            btn_frame, 
            text="🔄 RESET", 
            font=btn_font,
            width=12,
            height=2,
            bg="red",
            fg="white",
            command=self._on_reset_clicked
        )
        self.reset_btn.grid(row=0, column=2, padx=8, pady=5)

    def _create_settings(self):
        """Tạo phần cài đặt session"""
        settings_frame = tk.Frame(self.root, bg='black')
        settings_frame.pack(pady=5)

        # Session duration setting
        tk.Label(settings_frame, text="Duration:", fg="white", bg="black", font=("Arial", 9)).grid(row=0, column=0, padx=3)
        self.session_duration_var = tk.StringVar(value="1 hour")
        self.duration_combobox = tk.OptionMenu(
            settings_frame,
            self.session_duration_var,
            *SESSION_DURATION_OPTIONS.keys(),
            command=self._on_session_duration_changed
        )
        self.duration_combobox.config(
            font=("Arial", 8),
            width=8,
            bg="gray20",
            fg="white",
            highlightthickness=0
        )
        self.duration_combobox.grid(row=0, column=1, padx=3)

        # Target sessions setting
        tk.Label(settings_frame, text="Sessions:", fg="white", bg="black", font=("Arial", 9)).grid(row=0, column=2, padx=3)
        self.sessions_var = tk.StringVar(value="8")
        self.sessions_spinbox = tk.Spinbox(
            settings_frame,
            from_=1, to=20,
            textvariable=self.sessions_var,
            width=3,
            font=("Arial", 9),
            command=self._on_sessions_changed
        )
        self.sessions_spinbox.grid(row=0, column=3, padx=3)

        # Auto continue setting
        self.auto_continue_var = tk.BooleanVar(value=False)
        self.auto_continue_cb = tk.Checkbutton(
            settings_frame,
            text="Auto",
            variable=self.auto_continue_var,
            fg="white",
            bg="black",
            selectcolor="black",
            font=("Arial", 9),
            command=self._on_auto_continue_changed
        )
        self.auto_continue_cb.grid(row=0, column=4, padx=5)

        # Reset sessions button
        self.reset_sessions_btn = tk.Button(
            settings_frame,
            text="Reset",
            width=8,
            font=("Arial", 8),
            command=self._on_reset_sessions_clicked
        )
        self.reset_sessions_btn.grid(row=0, column=5, padx=5)
        
        # Debug toggle button (quick access)
        self.debug_toggle_btn = tk.Button(
            settings_frame,
            text="🧪",
            width=3,
            font=("Arial", 8),
            bg="#27ae60",
            fg="white",
            command=self._on_debug_toggle_clicked,
            relief="raised"
        )
        self.debug_toggle_btn.grid(row=0, column=6, padx=2)
        
        # Bind tooltip events
        def show_debug_tooltip(event):
            self.debug_status_label.config(text="🧪 Debug Mode Toggle (Ctrl+D)")
        
        def hide_debug_tooltip(event):
            if not self.is_debug_mode_active():
                self.debug_status_label.config(text="")
        
        self.debug_toggle_btn.bind("<Enter>", show_debug_tooltip)
        self.debug_toggle_btn.bind("<Leave>", hide_debug_tooltip)
        
        # Tooltip-like label for debug button (initially hidden)
        self.debug_status_label = tk.Label(
            settings_frame,
            text="",
            font=("Arial", 7),
            fg="red",
            bg="black"
        )
        self.debug_status_label.grid(row=1, column=0, columnspan=7, pady=2)

    def _on_debug_toggle_clicked(self):
        """Xử lý sự kiện click nút debug toggle"""
        if self.play_secondary_button_sound:
            self.play_secondary_button_sound()
        
        current_selection = self.session_duration_var.get()
        
        if current_selection.startswith("🧪"):
            # Currently in debug mode, switch to normal
            self.session_duration_var.set("1 hour")
            self.duration_combobox.config(bg="gray20", fg="white")
            self.debug_toggle_btn.config(bg="#27ae60", text="🧪")  # Green when debug available
            self.debug_status_label.config(text="")
            print("🔄 Switched from debug mode to normal mode (1 hour)")
            if self.on_session_duration_changed:
                duration_seconds = SESSION_DURATION_OPTIONS["1 hour"]
                self.on_session_duration_changed(duration_seconds, "1 hour", False)
        else:
            # Currently in normal mode, switch to debug
            self.session_duration_var.set("🧪 1 min (DEBUG)")
            self.duration_combobox.config(bg="#e74c3c", fg="white")
            self.debug_toggle_btn.config(bg="#c0392b", text="⚠️")  # Darker red when debug active
            self.debug_status_label.config(text="🧪 DEBUG MODE: 1-min sessions (not saved)")
            print("🧪 Switched to debug mode (1 minute sessions)")
            if self.on_session_duration_changed:
                duration_seconds = SESSION_DURATION_OPTIONS["🧪 1 min (DEBUG)"]
                self.on_session_duration_changed(duration_seconds, "🧪 1 min (DEBUG)", True)

    def _on_start_clicked(self):
        """Xử lý sự kiện click nút Start"""
        if self.play_main_button_sound:
            self.play_main_button_sound()
        if self.on_start:
            self.on_start()

    def _on_toggle_clicked(self):
        """Xử lý sự kiện click nút Pause/Resume"""
        if self.play_main_button_sound:
            self.play_main_button_sound()
        if self.on_toggle:
            self.on_toggle()

    def _on_reset_clicked(self):
        """Xử lý sự kiện click nút Reset"""
        if self.play_secondary_button_sound:
            self.play_secondary_button_sound()
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
        if self.play_secondary_button_sound:
            self.play_secondary_button_sound()
        if self.on_auto_continue_changed:
            self.on_auto_continue_changed(self.auto_continue_var.get())

    def _on_reset_sessions_clicked(self):
        """Xử lý sự kiện reset sessions"""
        if self.play_secondary_button_sound:
            self.play_secondary_button_sound()
        if self.on_reset_sessions:
            self.on_reset_sessions()

    def is_debug_mode_active(self):
        """Check if debug mode is currently active"""
        current_selection = self.session_duration_var.get()
        return current_selection.startswith("🧪")
    
    def reset_to_normal_mode(self):
        """Reset session duration to normal mode (1 hour)"""
        if self.is_debug_mode_active():
            print("🔄 Resetting from debug mode to normal mode")
            self.session_duration_var.set("1 hour")
            self.duration_combobox.config(bg="gray20", fg="white")
            # Trigger the change event
            if self.on_session_duration_changed:
                duration_seconds = SESSION_DURATION_OPTIONS["1 hour"]
                self.on_session_duration_changed(duration_seconds, "1 hour", False)

    def _on_session_duration_changed(self, selected_duration):
        """Xử lý sự kiện thay đổi session duration"""
        if self.play_sound:
            self.play_sound()
        
        # Check if debug mode is selected
        is_debug_mode = selected_duration.startswith("🧪")
        
        # Visual indicator for debug mode
        if is_debug_mode:
            self.duration_combobox.config(bg="#e74c3c", fg="white")  # Red background for debug
            self.debug_toggle_btn.config(bg="#c0392b", text="⚠️")  # Active debug button
            self.debug_status_label.config(text="🧪 DEBUG MODE: 1-min sessions (not saved)")
            print("🧪 DEBUG MODE ACTIVATED: 1-minute sessions")
            print("⚠️  This setting will NOT be saved to data files")
        else:
            self.duration_combobox.config(bg="gray20", fg="white")  # Normal background
            self.debug_toggle_btn.config(bg="#27ae60", text="🧪")  # Available debug button
            self.debug_status_label.config(text="")
        
        if self.on_session_duration_changed:
            duration_seconds = SESSION_DURATION_OPTIONS[selected_duration]
            self.on_session_duration_changed(duration_seconds, selected_duration, is_debug_mode)

    def _on_help_clicked(self):
        """Xử lý sự kiện click nút Help"""
        if self.play_secondary_button_sound:
            self.play_secondary_button_sound()
        if self.on_help_clicked:
            self.on_help_clicked()

    def _on_stats_clicked(self):
        """Xử lý sự kiện click nút Daily Stats"""
        if self.play_stats_button_sound:
            self.play_stats_button_sound()
        if self.on_stats_clicked:
            self.on_stats_clicked()

    def _on_mute_clicked(self):
        """Xử lý sự kiện click nút Mute"""
        if self.play_secondary_button_sound:
            self.play_secondary_button_sound()
        if self.on_mute_clicked:
            is_muted = self.on_mute_clicked()
            # Update button appearance based on mute state
            if is_muted:
                self.mute_btn.config(text="🔇 Muted", bg="#e74c3c")
            else:
                self.mute_btn.config(text="🔊 Sound", bg="#27ae60")

    def update_main_timer_display(self, time_text):
        """Cập nhật hiển thị main timer"""
        self.main_timer_label.config(text=time_text)

    def update_break_timer_display(self, time_text, break_session_seconds=0):
        """Cập nhật hiển thị break timer với màu sắc dựa trên hidden timer"""
        self.break_timer_label.config(text=f"Break: {time_text}")
        
        # Format hidden timer (MM:SS format)
        hidden_mins = break_session_seconds // 60
        hidden_secs = break_session_seconds % 60
        hidden_text = f"{hidden_mins:02d}:{hidden_secs:02d}"
        self.hidden_timer_label.config(text=hidden_text)
        
        # Change color based on current break session time
        if break_session_seconds >= 20 * 60:  # 20+ minutes: red color
            color = "red"
        elif break_session_seconds >= 10 * 60:  # 10+ minutes: magenta color
            color = "magenta"
        else:  # 0-10 minutes: cyan color
            color = "cyan"
        
        # Only change color when break timer is active
        if hasattr(self, '_break_timer_active') and self._break_timer_active:
            self.break_timer_label.config(fg=color)
            self.hidden_timer_label.config(fg=color)
        else:
            self.hidden_timer_label.config(fg="gray")

    def update_button_state(self, state):
        """Cập nhật trạng thái các nút theo dual clock system"""
        if state == "main_running":
            self.toggle_btn.config(text="🔄 → BREAK", bg="orange")
            self.main_timer_label.config(fg="lime")
            self.break_timer_label.config(fg="gray")
            self.hidden_timer_label.config(text="00:00", fg="gray")
            self._break_timer_active = False
        elif state == "break_running":
            self.toggle_btn.config(text="🔄 → MAIN", bg="blue")
            self.main_timer_label.config(fg="gray")
            self.break_timer_label.config(fg="cyan")
            self._break_timer_active = True
        elif state == "all_frozen":
            self.toggle_btn.config(text="▶ START", bg="green")
            self.main_timer_label.config(fg="white")
            self.break_timer_label.config(fg="white")
            self._break_timer_active = False
        elif state == "reset":
            self.toggle_btn.config(text="▶ START", bg="green")
            self.main_timer_label.config(text="00:00:00", fg="white")
            self.break_timer_label.config(text="Break: 00:00:00", fg="white")
            self.hidden_timer_label.config(text="00:00", fg="gray")
            self._break_timer_active = False

    def update_session_display(self, current, target):
        """Cập nhật hiển thị session"""
        self.session_label.config(text=f"Session: {current}/{target}")

    def update_progress_display(self, progress):
        """Cập nhật hiển thị tiến độ"""
        self.progress_label.config(text=f"Progress: {progress:.1f}%")

    def update_mute_button(self, is_muted):
        """Cập nhật trạng thái hiển thị nút mute"""
        if is_muted:
            self.mute_btn.config(text="🔇 Muted", bg="#e74c3c")
        else:
            self.mute_btn.config(text="🔊 Sound", bg="#27ae60")

    def show_session_complete_message(self):
        """Hiển thị thông báo hoàn thành một session"""
        print("🎯 Session complete message displayed")
        # No longer show messagebox because we have choice overlay
        # This message is only for compatibility with old code
        pass

    def show_all_sessions_complete_message(self):
        """Display message for all sessions complete - only console log, popup already integrated into overlay"""
        print("🎉 Target sessions achieved! Overlay will show celebration message.")
        # No longer show popup - notification already integrated into choice overlay
        pass

    def setup_task_callbacks(self):
        """Setup callbacks for task UI"""
        self.task_ui.on_add_task = self.on_add_task
        self.task_ui.on_complete_task = self.on_complete_task
        self.task_ui.on_delete_task = self.on_delete_task
        self.task_ui.on_edit_task = self.on_edit_task
        self.task_ui.on_reactivate_task = self.on_reactivate_task
        self.task_ui.on_move_task_up = self.on_move_task_up
        self.task_ui.on_move_task_down = self.on_move_task_down
        self.task_ui.on_clear_completed = self.on_clear_completed
        self.task_ui.play_sound = self.play_secondary_button_sound

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
            'main_timer_label': self.main_timer_label,
            'break_timer_label': self.break_timer_label,
            'hidden_timer_label': self.hidden_timer_label,
            'session_label': self.session_label,
            'progress_label': self.progress_label,
            'start_btn': self.start_btn,
            'toggle_btn': self.toggle_btn,
            'reset_btn': self.reset_btn,
            'sessions_spinbox': self.sessions_spinbox,
            'auto_continue_cb': self.auto_continue_cb,
            'task_ui': self.task_ui
        }

    def show_choice_overlay(self, current_session, target_sessions):
        """Hiển thị overlay lựa chọn session complete"""
        print(f"🎨 show_choice_overlay called: session {current_session}/{target_sessions}")
        
        # Debug: Check if root exists
        if not self.root:
            print("❌ Error: self.root is None!")
            return
        
        # Hide existing overlay if any
        if self.choice_overlay:
            print("🧹 Hiding existing overlay")
            self.hide_choice_overlay()
        
        print("🔧 Creating new overlay...")
        
        # Create overlay frame - adjust size to fit celebration message
        overlay_height = 230 if current_session >= target_sessions else 200  # Higher for celebration message
        self.choice_overlay = tk.Frame(self.root, bg='#34495e', relief='raised', bd=1)
        self.choice_overlay.place(relx=0.5, rely=0.5, anchor='center', width=380, height=overlay_height)
        
        print(f"✅ Overlay frame created: {self.choice_overlay}")
        
        # Background with dark color and special effect for celebration
        if current_session >= target_sessions:
            # Celebration mode: gold border effect
            overlay_bg = tk.Frame(self.choice_overlay, bg='#2c3e50', relief='solid', bd=2)
            overlay_bg.config(highlightbackground="#f39c12", highlightthickness=1)
        else:
            # Normal mode
            overlay_bg = tk.Frame(self.choice_overlay, bg='#2c3e50', relief='flat', bd=0)
        overlay_bg.pack(fill='both', expand=True, padx=3, pady=3)
        
        # Title - improved logic for session display with celebration message
        if current_session >= target_sessions:
            title_text = "🎉 TARGET ACHIEVED! 🎉"
            title_color = "#f39c12"
            if current_session == target_sessions:
                # Just reached target for the first time
                message_text = (f"🏆 Congratulations! You completed {target_sessions} sessions! 🏆\n"
                               f"🌟 You are a productivity champion! 🌟\n"
                               f"✨ Continue to go BEYOND your target! ✨")
            else:
                # Already exceeded target
                message_text = (f"🚀 Amazing! Session {current_session}/{target_sessions} complete! 🚀\n"
                               f"🌟 You're in EXTRA MODE! 🌟\n"
                               f"💪 Keep pushing your limits! 💪")
        else:
            title_text = "� Session Complete! �"
            title_color = "#27ae60"
            message_text = f"Session {current_session}/{target_sessions} completed!\n💡 What's next? 💡"
        
        title_label = tk.Label(
            overlay_bg,
            text=title_text,
            font=("Arial", 12, "bold"),  # Reduced from 13 to 12 to make space for message
            fg=title_color,
            bg='#2c3e50'
        )
        title_label.pack(pady=(10, 4))  # Reduced padding to make space for longer message
        
        # Message with better line height for celebration text
        message_font_size = 8 if current_session >= target_sessions else 9  # Smaller for celebration
        message_label = tk.Label(
            overlay_bg,
            text=message_text,
            font=("Arial", message_font_size),
            fg="white",
            bg='#2c3e50',
            justify='center',
            wraplength=340  # Wrap text to fit within overlay
        )
        message_label.pack(pady=(0, 10))  # Moderate bottom padding
        
        # Buttons frame with grid layout for better balance
        buttons_frame = tk.Frame(overlay_bg, bg='#2c3e50')
        buttons_frame.pack(pady=(0, 8), padx=12, fill='x')  # Bottom and side padding
        
        # Configure grid so buttons have even spacing
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        
        # Continue button with context-appropriate text
        continue_text = "🚀 Keep Going!" if current_session >= target_sessions else "✅ Continue"
        continue_btn = tk.Button(
            buttons_frame,
            text=continue_text,
            font=("Arial", 9, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#2ecc71",
            activeforeground="white",
            width=11,
            height=1,
            pady=6,
            relief='flat',
            bd=0,
            command=self._on_continue_clicked
        )
        continue_btn.grid(row=0, column=0, padx=(0, 4), sticky='ew')
        
        # Break button with context-appropriate text  
        break_text = "🎉 Celebrate!" if current_session >= target_sessions else "☕ Break"
        break_btn = tk.Button(
            buttons_frame,
            text=break_text,
            font=("Arial", 9, "bold"),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            activeforeground="white",
            width=11,
            height=1,
            pady=6,
            relief='flat',
            bd=0,
            command=self._on_break_clicked
        )
        break_btn.grid(row=0, column=1, padx=(4, 0), sticky='ew')
        
        # Bring overlay to front with tkraise and focus
        self.choice_overlay.tkraise()
        self.choice_overlay.lift()
        
        # Bring root window to front and focus
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.attributes('-topmost', False)  # Just flash to front then return to normal
        
        # Focus on continue button
        continue_btn.focus_set()
        continue_btn.bind('<Return>', lambda e: self._on_continue_clicked())
        break_btn.bind('<Return>', lambda e: self._on_break_clicked())
        
        print("✅ Choice overlay setup complete!")
        print(f"🔍 Overlay geometry: {self.choice_overlay.winfo_reqwidth()}x{self.choice_overlay.winfo_reqheight()}")
        
        # Force update
        self.root.update_idletasks()

    def hide_choice_overlay(self):
        """Ẩn overlay lựa chọn"""
        if self.choice_overlay:
            self.choice_overlay.destroy()
            self.choice_overlay = None

    def _on_continue_clicked(self):
        """Xử lý khi user click Continue"""
        print("🎯 Continue button clicked!")
        self.hide_choice_overlay()
        if self.on_continue_session:
            print("🔄 Calling on_continue_session callback...")
            try:
                self.on_continue_session()
                print("✅ on_continue_session callback completed")
            except Exception as e:
                print(f"❌ Error in on_continue_session callback: {e}")
        else:
            print("❌ on_continue_session callback is None!")

    def _on_break_clicked(self):
        """Xử lý khi user click Take Break"""
        print("☕ Break button clicked!")
        self.hide_choice_overlay()
        if self.on_take_break:
            print("🔄 Calling on_take_break callback...")
            try:
                self.on_take_break()
                print("✅ on_take_break callback completed")
            except Exception as e:
                print(f"❌ Error in on_take_break callback: {e}")
        else:
            print("❌ on_take_break callback is None!")

    # State restoration methods for timer state manager
    def set_target_sessions(self, sessions):
        """Set target sessions value"""
        self.sessions_var.set(str(sessions))

    def set_session_duration(self, duration_seconds):
        """Set session duration value"""
        # Convert seconds to appropriate dropdown value
        if duration_seconds == 900:  # 15 minutes
            self.session_duration_var.set("15 min")
        elif duration_seconds == 1200:  # 20 minutes
            self.session_duration_var.set("20 min")
        elif duration_seconds == 1500:  # 25 minutes  
            self.session_duration_var.set("25 min")
        elif duration_seconds == 1800:  # 30 minutes
            self.session_duration_var.set("30 min")
        elif duration_seconds == 2700:  # 45 minutes
            self.session_duration_var.set("45 min")
        elif duration_seconds == 3600:  # 1 hour
            self.session_duration_var.set("1 hour")
        elif duration_seconds == 5400:  # 1.5 hours
            self.session_duration_var.set("1.5 hours")
        elif duration_seconds == 7200:  # 2 hours
            self.session_duration_var.set("2 hours")
        else:
            # Default to 1 hour if unknown duration
            self.session_duration_var.set("1 hour")

    def set_auto_continue(self, auto_continue):
        """Set auto continue checkbox value"""
        self.auto_continue_var.set(auto_continue)

    def show_restore_session_overlay(self, callback):
        """Show overlay for session restoration choice"""
        print("🔄 Showing restore session overlay...")
        
        # Hide existing overlay if any
        if hasattr(self, 'restore_overlay') and self.restore_overlay:
            self.restore_overlay.destroy()
        
        # Create overlay frame
        self.restore_overlay = tk.Frame(self.root, bg='#34495e', relief='raised', bd=1)
        self.restore_overlay.place(relx=0.5, rely=0.5, anchor='center', width=400, height=250)
        
        # Background
        overlay_bg = tk.Frame(self.restore_overlay, bg='#2c3e50', relief='flat', bd=0)
        overlay_bg.pack(fill='both', expand=True, padx=3, pady=3)
        
        # Icon and title
        title_label = tk.Label(
            overlay_bg,
            text="💾 Session Recovery",
            font=("Arial", 14, "bold"),
            fg="#3498db",
            bg='#2c3e50'
        )
        title_label.pack(pady=(15, 10))
        
        # Message
        message_text = ("Found a saved timer session from today.\n\n"
                       "Would you like to restore your previous session?\n\n"
                       "This will restore:\n"
                       "• Timer values (main time, break time)\n"
                       "• Session progress\n"
                       "• Timer state (running/paused)")
        
        message_label = tk.Label(
            overlay_bg,
            text=message_text,
            font=("Arial", 9),
            fg="white",
            bg='#2c3e50',
            justify='center',
            wraplength=360
        )
        message_label.pack(pady=(0, 15))
        
        # Buttons frame
        buttons_frame = tk.Frame(overlay_bg, bg='#2c3e50')
        buttons_frame.pack(pady=(0, 15), padx=20, fill='x')
        
        # Configure grid
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        
        # Restore button
        restore_btn = tk.Button(
            buttons_frame,
            text="✅ Restore Session",
            font=("Arial", 10, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#2ecc71",
            activeforeground="white",
            width=15,
            height=2,
            relief='flat',
            bd=0,
            command=lambda: self._on_restore_clicked(callback, True)
        )
        restore_btn.grid(row=0, column=0, padx=(0, 5), sticky='ew')
        
        # Start fresh button
        fresh_btn = tk.Button(
            buttons_frame,
            text="🆕 Start Fresh",
            font=("Arial", 10, "bold"),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            activeforeground="white",
            width=15,
            height=2,
            relief='flat',
            bd=0,
            command=lambda: self._on_restore_clicked(callback, False)
        )
        fresh_btn.grid(row=0, column=1, padx=(5, 0), sticky='ew')
        
        # Bring overlay to front
        self.restore_overlay.tkraise()
        self.restore_overlay.lift()
        
        # Focus on restore button by default
        restore_btn.focus_set()
        restore_btn.bind('<Return>', lambda e: self._on_restore_clicked(callback, True))
        fresh_btn.bind('<Return>', lambda e: self._on_restore_clicked(callback, False))
        
        # Keyboard shortcuts
        self.root.bind('<Key-y>', lambda e: self._on_restore_clicked(callback, True))
        self.root.bind('<Key-n>', lambda e: self._on_restore_clicked(callback, False))
        self.root.bind('<Escape>', lambda e: self._on_restore_clicked(callback, False))
        
        print("✅ Restore session overlay displayed")

    def _on_restore_clicked(self, callback, restore_choice):
        """Handle restore session overlay button clicks"""
        print(f"🔄 Restore choice: {'Yes' if restore_choice else 'No'}")
        
        # Unbind keyboard shortcuts
        self.root.unbind('<Key-y>')
        self.root.unbind('<Key-n>')
        self.root.unbind('<Escape>')
        
        # Hide overlay
        if hasattr(self, 'restore_overlay') and self.restore_overlay:
            self.restore_overlay.destroy()
            self.restore_overlay = None
        
        # Call callback with choice
        if callback:
            callback(restore_choice)

    def hide_restore_session_overlay(self):
        """Hide restore session overlay"""
        if hasattr(self, 'restore_overlay') and self.restore_overlay:
            self.restore_overlay.destroy()
            self.restore_overlay = None
