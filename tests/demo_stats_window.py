#!/usr/bin/env python3
"""
Demo Daily Stats Window
Thử nghiệm cửa sổ thống kê hàng ngày
"""

import sys
import os
import tkinter as tk
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.managers.daily_stats_manager import DailyStatsManager
from src.ui.daily_stats_window import DailyStatsWindow

def demo_daily_stats_window():
    """Demo cửa sổ daily stats"""
    # Tạo dữ liệu demo
    stats = DailyStatsManager()
    
    # Thêm dữ liệu demo
    stats.update_study_time(3600)  # 1 giờ
    stats.update_break_time(900)   # 15 phút
    stats.increment_sessions_completed()
    stats.increment_sessions_completed()
    stats.increment_tasks_completed()
    stats.increment_tasks_completed()
    stats.increment_tasks_completed()
    
    # Tạo root window
    root = tk.Tk()
    root.title("Demo - Daily Stats")
    root.geometry("300x200")
    
    # Tạo nút để mở daily stats
    open_btn = tk.Button(
        root,
        text="📊 Open Daily Stats Window",
        command=lambda: DailyStatsWindow(root, stats).show(),
        font=("Arial", 12, "bold"),
        bg="#2c3e50",
        fg="white",
        padx=20,
        pady=10
    )
    open_btn.pack(expand=True)
    
    info_label = tk.Label(
        root,
        text="Click the button above to\nopen the Daily Stats window",
        font=("Arial", 10),
        fg="gray"
    )
    info_label.pack(pady=10)
    
    print("🚀 Starting Daily Stats Window Demo...")
    print("📊 Demo data added to today's stats:")
    summary = stats.get_today_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    root.mainloop()

if __name__ == "__main__":
    demo_daily_stats_window()
