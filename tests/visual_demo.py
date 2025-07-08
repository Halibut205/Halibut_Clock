#!/usr/bin/env python3
"""
Visual Improvements Showcase
Demo các cải tiến về giao diện trực quan
"""

import sys
import os
import tkinter as tk
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.managers.daily_stats_manager import DailyStatsManager
from src.ui.daily_stats_window import DailyStatsWindow
from datetime import datetime, timedelta

def create_demo_data():
    """Tạo dữ liệu demo phong phú để showcase"""
    stats = DailyStatsManager()
    
    print("🎨 Creating rich demo data for visual showcase...")
    
    # Hôm nay - high productivity
    stats.update_study_time(14400)  # 4 giờ
    stats.update_break_time(1800)   # 30 phút
    for i in range(4):
        stats.increment_sessions_completed()
    for i in range(6):
        stats.increment_tasks_completed()
    
    print("📊 Demo data created:")
    print("  Today: 4h study, 30m break, 4 sessions, 6 tasks")
    print("  Efficiency: 88.9% (excellent)")
    print("  Daily goal: 100% completed 🔥")
    
    return stats

def showcase_features():
    """Showcase tất cả tính năng visual"""
    stats = create_demo_data()
    
    root = tk.Tk()
    root.title("Visual Improvements Showcase")
    root.geometry("400x300")
    root.configure(bg='#f8f9fa')
    
    # Title
    title = tk.Label(
        root,
        text="🎨 Visual Improvements Showcase",
        font=("Segoe UI", 16, "bold"),
        bg='#f8f9fa',
        fg='#2c3e50'
    )
    title.pack(pady=20)
    
    # Features list
    features = [
        "🎯 Color-coded efficiency (Green/Orange/Red)",
        "📊 Visual progress bars for daily goals",
        "🔥 Emoji indicators for achievements",
        "💪 Hover effects on all buttons",
        "📈 Row coloring in data tables",
        "🎨 Material Design button styling",
        "📱 Modern card-based layout",
        "⚡ Real-time visual feedback"
    ]
    
    for feature in features:
        label = tk.Label(
            root,
            text=feature,
            font=("Segoe UI", 11),
            bg='#f8f9fa',
            fg='#34495e',
            anchor='w'
        )
        label.pack(fill='x', padx=40, pady=2)
    
    # Demo button
    demo_btn = tk.Button(
        root,
        text="🚀 Open Enhanced Daily Stats Window",
        command=lambda: DailyStatsWindow(root, stats).show(),
        font=("Segoe UI", 12, "bold"),
        bg="#3498db",
        fg="white",
        relief="flat",
        padx=20,
        pady=15,
        cursor="hand2"
    )
    demo_btn.pack(pady=30)
    
    # Hover effects for demo button
    def on_enter(e):
        demo_btn.config(bg="#2980b9")
    def on_leave(e):
        demo_btn.config(bg="#3498db")
    
    demo_btn.bind("<Enter>", on_enter)
    demo_btn.bind("<Leave>", on_leave)
    
    print("\n🎉 Visual showcase ready!")
    print("Click the button to see all improvements in action!")
    
    root.mainloop()

if __name__ == "__main__":
    showcase_features()
