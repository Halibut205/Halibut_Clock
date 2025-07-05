# -*- coding: utf-8 -*-
"""
Main Application - Entry point của ứng dụng
"""

import tkinter as tk
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.timer_controller import TimerController
from src.ui.welcome_screen import show_welcome_screen
from src.ui.app_settings import should_show_welcome

class FliqloTimerApp:
    def __init__(self):
        self.root = None
        self.controller = None

    def start_main_timer(self):
        """Khởi tạo và chạy main timer app"""
        self.root = tk.Tk()
        self.controller = TimerController(self.root)
        self.run()

    def run(self):
        """Chạy ứng dụng chính"""
        if self.root:
            self.root.mainloop()

def main():
    """Entry point của ứng dụng"""
    app = FliqloTimerApp()
    
    # Check if should show welcome screen
    if should_show_welcome():
        # Hiển thị welcome screen trước
        show_welcome_screen(app.start_main_timer)
    else:
        # Chạy trực tiếp main timer
        app.start_main_timer()

if __name__ == "__main__":
    main()
