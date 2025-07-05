"""
UI Components Module - Quản lý giao diện người dùng
"""

import tkinter as tk
from tkinter import font as tkfont

class FliqloUI:
    def __init__(self, root):
        self.root = root
        self._setup_window()
        self._create_widgets()
        
        # Callbacks cho các sự kiện
        self.on_start = None
        self.on_toggle = None
        self.on_reset = None
        
        # Sound manager callback
        self.play_sound = None

    def _setup_window(self):
        """Thiết lập cửa sổ chính"""
        self.root.title("Fliqlo Timer")
        self.root.configure(bg='black')
        self.root.geometry("600x300")

    def _create_widgets(self):
        """Tạo các widget UI"""
        # Font lớn, đậm, dễ đọc kiểu Fliqlo
        self.clock_font = tkfont.Font(family="Courier New", size=72, weight="bold")
        self.break_font = tkfont.Font(family="Courier New", size=36, weight="bold")

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

        # Button frame
        self._create_buttons()

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

    def get_widgets(self):
        """Trả về dictionary chứa các widget chính"""
        return {
            'timer_label': self.timer_label,
            'break_label': self.break_label,
            'start_btn': self.start_btn,
            'toggle_btn': self.toggle_btn,
            'reset_btn': self.reset_btn
        }
