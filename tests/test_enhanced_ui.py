"""
Test script for Enhanced Daily Statistics UI
"""
import tkinter as tk
from datetime import datetime, timedelta
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from managers.daily_stats_manager import DailyStatsManager
from ui.daily_stats_window import DailyStatsWindow

def create_demo_data():
    """Tạo dữ liệu demo để test UI"""
    stats_manager = DailyStatsManager("demo_data")
    
    # Tạo dữ liệu cho hôm nay
    stats_manager.update_study_time(3 * 3600 + 30 * 60)  # 3.5 hours
    stats_manager.update_break_time(45 * 60)  # 45 minutes
    
    # Tạo sessions và tasks
    for i in range(6):
        stats_manager.increment_sessions_completed()
    
    for i in range(8):
        stats_manager.increment_tasks_completed()
    
    # Tạo dữ liệu cho vài ngày trước
    import json
    from datetime import date
    
    # Yesterday
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    stats_manager.stats_data[yesterday] = {
        "date": yesterday,
        "study_time": 2 * 3600,  # 2 hours
        "break_time": 30 * 60,   # 30 minutes
        "sessions_completed": 4,
        "tasks_completed": 5,
        "start_time": "2025-07-07T09:00:00",
        "last_update": "2025-07-07T17:00:00"
    }
    
    # Day before yesterday
    day_before = (date.today() - timedelta(days=2)).isoformat()
    stats_manager.stats_data[day_before] = {
        "date": day_before,
        "study_time": 4 * 3600 + 15 * 60,  # 4.25 hours
        "break_time": 1 * 3600,  # 1 hour
        "sessions_completed": 8,
        "tasks_completed": 12,
        "start_time": "2025-07-06T08:30:00",
        "last_update": "2025-07-06T18:30:00"
    }
    
    # More demo data for the week
    for i in range(3, 7):
        demo_date = (date.today() - timedelta(days=i)).isoformat()
        stats_manager.stats_data[demo_date] = {
            "date": demo_date,
            "study_time": (2 + i * 0.5) * 3600,  # Varying study time
            "break_time": 30 * 60,
            "sessions_completed": 3 + i,
            "tasks_completed": 4 + i,
            "start_time": f"2025-07-{8-i:02d}T09:00:00",
            "last_update": f"2025-07-{8-i:02d}T17:00:00"
        }
    
    stats_manager.save_stats()
    return stats_manager

def main():
    """Main demo function"""
    # Create root window
    root = tk.Tk()
    root.title("Enhanced Daily Statistics Demo")
    root.geometry("400x300")
    root.configure(bg='#f5f5f5')
    
    # Create demo data
    stats_manager = create_demo_data()
    
    # Create info label
    info_label = tk.Label(
        root,
        text="Enhanced Daily Statistics Demo\n\n" +
             "This demo shows the improved UI with:\n" +
             "• Progress bars and visual indicators\n" +
             "• Trend comparisons vs yesterday\n" +
             "• Achievement badges\n" +
             "• Motivational messages\n" +
             "• Enhanced tooltips\n" +
             "• Better color coding\n" +
             "• ASCII charts\n\n" +
             "Click the button below to open the stats window:",
        font=("Segoe UI", 11),
        bg='#f5f5f5',
        fg='#2c3e50',
        justify='left'
    )
    info_label.pack(pady=20, padx=20)
    
    # Create button to open stats window
    def open_stats():
        stats_window = DailyStatsWindow(root, stats_manager)
        stats_window.show()
    
    open_button = tk.Button(
        root,
        text="📊 Open Enhanced Statistics",
        command=open_stats,
        font=("Segoe UI", 12, "bold"),
        bg='#3498db',
        fg='white',
        relief='flat',
        bd=0,
        padx=20,
        pady=10,
        cursor='hand2'
    )
    open_button.pack(pady=20)
    
    # Add hover effects
    def on_enter(e):
        open_button.config(bg='#2980b9')
    
    def on_leave(e):
        open_button.config(bg='#3498db')
    
    open_button.bind("<Enter>", on_enter)
    open_button.bind("<Leave>", on_leave)
    
    # Cleanup function
    def cleanup():
        # Clean up demo data
        import shutil
        if os.path.exists("demo_data"):
            shutil.rmtree("demo_data")
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", cleanup)
    
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()
