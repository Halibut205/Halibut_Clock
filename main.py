"""
Main Application - Entry point của ứng dụng
"""

import tkinter as tk
from timer_controller import TimerController

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
