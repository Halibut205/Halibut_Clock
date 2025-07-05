"""
Main Application - Entry point của ứng dụng
"""

import tkinter as tk
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.timer_controller import TimerController

class FliqloTimerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.controller = TimerController(self.root)

    def run(self):
        """Chạy ứng dụng"""
        self.root.mainloop()

def main():
    """Entry point của ứng dụng"""
    app = FliqloTimerApp()
    app.run()

if __name__ == "__main__":
    main()
