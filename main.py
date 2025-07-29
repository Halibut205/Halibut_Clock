#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Study Timer - Main Application Entry Point
A beautiful Pomodoro timer with dual clock system and unlimited sessions support.
"""

import sys
import os
import tkinter as tk
from typing import Optional

# Console window management for production deployment
if sys.executable.endswith('pythonw.exe'):
    # Running with pythonw.exe - console already hidden
    pass
elif '--hide-console' in sys.argv:
    # Hide console window on Windows
    try:
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except ImportError:
        pass

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.timer_controller import TimerController
from src.ui.welcome_screen import show_welcome_screen
from src.ui.app_settings import should_show_welcome


class StudyTimerApp:
    """Main application class for the Study Timer"""
    
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
    app = StudyTimerApp()
    
    # Check if should show welcome screen
    if should_show_welcome():
        # Hiển thị welcome screen trước
        show_welcome_screen(app.start_main_timer)
    else:
        # Chạy trực tiếp main timer
        app.start_main_timer()

if __name__ == "__main__":
    main()
