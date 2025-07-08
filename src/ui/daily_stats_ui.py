"""
Daily Statistics UI - Giao diện hiển thị thống kê học tập hàng ngày
"""
import tkinter as tk
from tkinter import ttk
from datetime import datetime

class DailyStatsUI:
    def __init__(self, parent):
        self.parent = parent
        self.stats_manager = None  # Sẽ được set từ bên ngoài
        
        # Callbacks
        self.on_reset_today = None
        
        self.create_ui()
    
    def create_ui(self):
        """Tạo giao diện thống kê"""
        # Main frame
        self.main_frame = ttk.LabelFrame(self.parent, text="📊 Daily Statistics", padding="10")
        self.main_frame.pack(fill="x", padx=10, pady=5)
        
        # Today stats frame
        self.today_frame = tk.Frame(self.main_frame)
        self.today_frame.pack(fill="x", pady=(0, 10))
        
        # Today's statistics
        self.create_today_stats()
        
        # Controls frame
        self.controls_frame = tk.Frame(self.main_frame)
        self.controls_frame.pack(fill="x", pady=(0, 10))
        
        # Refresh button
        self.refresh_btn = tk.Button(
            self.controls_frame,
            text="🔄 Refresh",
            command=self.refresh_stats,
            bg="#e3f2fd",
            fg="#1976d2",
            relief="flat",
            padx=10
        )
        self.refresh_btn.pack(side="left", padx=(0, 5))
        
        # Reset today button
        self.reset_btn = tk.Button(
            self.controls_frame,
            text="🗑️ Reset Today",
            command=self._on_reset_today,
            bg="#ffebee",
            fg="#d32f2f",
            relief="flat",
            padx=10
        )
        self.reset_btn.pack(side="left", padx=5)
        
        # Weekly summary frame (collapsible)
        self.weekly_frame = ttk.LabelFrame(self.main_frame, text="📈 Weekly Summary", padding="5")
        self.weekly_frame.pack(fill="x", pady=(10, 0))
        
        self.create_weekly_stats()
    
    def create_today_stats(self):
        """Tạo phần hiển thị thống kê hôm nay"""
        # Date label
        self.date_label = tk.Label(
            self.today_frame,
            text=f"Today: {datetime.now().strftime('%Y-%m-%d')}",
            font=("Arial", 12, "bold"),
            fg="#1976d2"
        )
        self.date_label.pack(anchor="w")
        
        # Stats grid
        self.stats_grid = tk.Frame(self.today_frame)
        self.stats_grid.pack(fill="x", pady=(5, 0))
        
        # Study time
        self.study_label = tk.Label(self.stats_grid, text="📚 Study Time:", font=("Arial", 10))
        self.study_label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        self.study_value = tk.Label(
            self.stats_grid, 
            text="00:00:00", 
            font=("Arial", 10, "bold"),
            fg="#2e7d32"
        )
        self.study_value.grid(row=0, column=1, sticky="w")
        
        # Break time
        self.break_label = tk.Label(self.stats_grid, text="☕ Break Time:", font=("Arial", 10))
        self.break_label.grid(row=0, column=2, sticky="w", padx=(20, 10))
        
        self.break_value = tk.Label(
            self.stats_grid, 
            text="00:00:00", 
            font=("Arial", 10, "bold"),
            fg="#f57c00"
        )
        self.break_value.grid(row=0, column=3, sticky="w")
        
        # Sessions completed
        self.sessions_label = tk.Label(self.stats_grid, text="🎯 Sessions:", font=("Arial", 10))
        self.sessions_label.grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(5, 0))
        
        self.sessions_value = tk.Label(
            self.stats_grid, 
            text="0", 
            font=("Arial", 10, "bold"),
            fg="#7b1fa2"
        )
        self.sessions_value.grid(row=1, column=1, sticky="w", pady=(5, 0))
        
        # Tasks completed
        self.tasks_label = tk.Label(self.stats_grid, text="✅ Tasks:", font=("Arial", 10))
        self.tasks_label.grid(row=1, column=2, sticky="w", padx=(20, 10), pady=(5, 0))
        
        self.tasks_value = tk.Label(
            self.stats_grid, 
            text="0", 
            font=("Arial", 10, "bold"),
            fg="#d32f2f"
        )
        self.tasks_value.grid(row=1, column=3, sticky="w", pady=(5, 0))
    
    def create_weekly_stats(self):
        """Tạo phần hiển thị thống kê tuần"""
        self.weekly_grid = tk.Frame(self.weekly_frame)
        self.weekly_grid.pack(fill="x")
        
        # Weekly total study time
        self.weekly_study_label = tk.Label(self.weekly_grid, text="📚 Week Study:", font=("Arial", 9))
        self.weekly_study_label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        self.weekly_study_value = tk.Label(
            self.weekly_grid, 
            text="00:00:00", 
            font=("Arial", 9, "bold"),
            fg="#2e7d32"
        )
        self.weekly_study_value.grid(row=0, column=1, sticky="w")
        
        # Weekly active days
        self.weekly_days_label = tk.Label(self.weekly_grid, text="📅 Active Days:", font=("Arial", 9))
        self.weekly_days_label.grid(row=0, column=2, sticky="w", padx=(15, 10))
        
        self.weekly_days_value = tk.Label(
            self.weekly_grid, 
            text="0/7", 
            font=("Arial", 9, "bold"),
            fg="#1976d2"
        )
        self.weekly_days_value.grid(row=0, column=3, sticky="w")
        
        # Average daily study
        self.avg_study_label = tk.Label(self.weekly_grid, text="📊 Daily Avg:", font=("Arial", 9))
        self.avg_study_label.grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(5, 0))
        
        self.avg_study_value = tk.Label(
            self.weekly_grid, 
            text="00:00:00", 
            font=("Arial", 9, "bold"),
            fg="#7b1fa2"
        )
        self.avg_study_value.grid(row=1, column=1, sticky="w", pady=(5, 0))
        
        # Total sessions this week
        self.weekly_sessions_label = tk.Label(self.weekly_grid, text="🎯 Sessions:", font=("Arial", 9))
        self.weekly_sessions_label.grid(row=1, column=2, sticky="w", padx=(15, 10), pady=(5, 0))
        
        self.weekly_sessions_value = tk.Label(
            self.weekly_grid, 
            text="0", 
            font=("Arial", 9, "bold"),
            fg="#f57c00"
        )
        self.weekly_sessions_value.grid(row=1, column=3, sticky="w", pady=(5, 0))
    
    def set_stats_manager(self, stats_manager):
        """Set reference to stats manager"""
        self.stats_manager = stats_manager
        self.refresh_stats()
    
    def refresh_stats(self):
        """Cập nhật hiển thị thống kê"""
        if not self.stats_manager:
            return
        
        # Update today's stats
        today_summary = self.stats_manager.get_today_summary()
        self.study_value.config(text=today_summary["study_time"])
        self.break_value.config(text=today_summary["break_time"])
        self.sessions_value.config(text=today_summary["sessions_completed"])
        self.tasks_value.config(text=today_summary["tasks_completed"])
        
        # Update weekly stats
        weekly_summary = self.stats_manager.get_weekly_total()
        self.weekly_study_value.config(text=weekly_summary["total_study_time"])
        self.weekly_days_value.config(text=f"{weekly_summary['days_active']}/7")
        self.avg_study_value.config(text=weekly_summary["average_daily_study"])
        self.weekly_sessions_value.config(text=str(weekly_summary["total_sessions"]))
        
        # Update date
        self.date_label.config(text=f"Today: {datetime.now().strftime('%Y-%m-%d')}")
    
    def _on_reset_today(self):
        """Xử lý khi click reset today"""
        if self.on_reset_today:
            self.on_reset_today()
        self.refresh_stats()
    
    def get_ui_components(self):
        """Trả về các component UI để có thể ẩn/hiện"""
        return {
            'main_frame': self.main_frame,
            'refresh_btn': self.refresh_btn,
            'reset_btn': self.reset_btn
        }
