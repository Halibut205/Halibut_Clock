"""
Daily Statistics Window - Cửa sổ thống kê học tập hàng ngày riêng biệt
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta, date
import calendar
import shutil
import os

# Import matplotlib for charts
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.dates as mdates
    from matplotlib.figure import Figure
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

class DailyStatsWindow:
    def __init__(self, parent, stats_manager):
        self.parent = parent
        self.stats_manager = stats_manager
        self.window = None
        self.current_data = []  # Để lưu dữ liệu hiện tại trong Data Explorer
        
        # Overlay variables
        self.date_overlay = None
        self.overlay_visible = False
        
    def show(self):
        """Hiển thị cửa sổ thống kê"""
        if self.window is not None:
            # Nếu cửa sổ đã mở, chỉ cần bring to front
            self.window.lift()
            self.window.focus_force()
            self.refresh_data()
            return
            
        # Tạo cửa sổ mới với kích thước lớn hơn
        self.window = tk.Toplevel(self.parent)
        self.window.title("📊 Daily Statistics - Study Timer")
        self.window.geometry("1200x800")  # Tăng từ 800x600 lên 1200x800
        self.window.configure(bg='#f5f5f5')
        
        # Đặt icon và không cho resize quá nhỏ
        self.window.minsize(1000, 700)  # Tăng minsize từ 700x500 lên 1000x700
        
        # Xử lý khi đóng cửa sổ
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.create_widgets()
        self.refresh_data()
        
        # Center window
        self.center_window()
    
    def center_window(self):
        """Căn giữa cửa sổ"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Tạo các widget trong cửa sổ"""
        # Main container
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="📊 Daily Learning Statistics",
            font=("Arial", 16, "bold"),
            bg='#f5f5f5',
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 15))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True)
        
        # Tab 1: Today's Summary
        self.create_today_tab()
        
        # Tab 2: Weekly Overview
        self.create_weekly_tab()
        
        # Tab 3: Monthly Overview
        self.create_monthly_tab()
        
        # Tab 4: History & Charts
        self.create_history_tab()
        
        # Tab 5: Yearly Overview
        self.create_yearly_tab()
        
        # Tab 6: All Data Explorer
        self.create_data_explorer_tab()
        
        # Control buttons frame
        self.create_control_buttons(main_frame)
    
    def create_today_tab(self):
        """Tạo tab thống kê hôm nay"""
        today_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(today_frame, text="📅 Today")
        
        # Date header
        date_label = tk.Label(
            today_frame,
            text=f"Today: {datetime.now().strftime('%A, %B %d, %Y')}",
            font=("Arial", 14, "bold"),
            bg='white',
            fg='#34495e'
        )
        date_label.pack(fill="x", pady=(0, 20))
        
        # Stats grid
        stats_frame = tk.Frame(today_frame, bg='white')
        stats_frame.pack(fill="x", pady=(0, 20))
        
        # Study time card
        self.create_stat_card(stats_frame, "📚 Study Time", "study_time", "#27ae60", 0, 0)
        
        # Break time card
        self.create_stat_card(stats_frame, "☕ Break Time", "break_time", "#e67e22", 0, 1)
        
        # Sessions card
        self.create_stat_card(stats_frame, "🎯 Sessions", "sessions", "#8e44ad", 1, 0)
        
        # Tasks card
        self.create_stat_card(stats_frame, "✅ Tasks", "tasks", "#e74c3c", 1, 1)
        
        # Progress summary
        self.create_progress_summary(today_frame)
        
        # Motivational message section
        self.create_motivational_section(today_frame)
        
        # Achievement badges section
        self.create_achievement_section(today_frame)
    
    def create_stat_card(self, parent, title, stat_type, color, row, col):
        """Tạo card thống kê với thiết kế đẹp hơn và progress indicators"""
        # Outer container với shadow effect
        outer_frame = tk.Frame(parent, bg='#ecf0f1', relief="raised", bd=1)
        outer_frame.grid(row=row, column=col, padx=12, pady=12, sticky="nsew", ipadx=3, ipady=3)
        
        # Inner card với gradient-like effect
        card_frame = tk.Frame(outer_frame, bg=color, relief="flat", bd=0)
        card_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Configure grid weights
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        # Icon and title frame
        header_frame = tk.Frame(card_frame, bg=color)
        header_frame.pack(fill="x", pady=(15, 5))
        
        # Title with better typography
        title_label = tk.Label(
            header_frame,
            text=title,
            font=("Segoe UI", 11, "bold"),
            bg=color,
            fg="white"
        )
        title_label.pack()
        
        # Value with larger, more readable font
        value_label = tk.Label(
            card_frame,
            text="--:--:--" if stat_type in ["study_time", "break_time"] else "0",
            font=("Consolas", 20, "bold"),  # Monospace font for better number display
            bg=color,
            fg="white"
        )
        value_label.pack(pady=(0, 5))
        
        # Visual indicator and trend
        indicator_frame = tk.Frame(card_frame, bg=color)
        indicator_frame.pack(fill="x", pady=(0, 10))
        
        # Trend arrow and percentage
        trend_label = tk.Label(
            indicator_frame,
            text="📊 vs yesterday",
            font=("Segoe UI", 9),
            bg=color,
            fg="white"
        )
        trend_label.pack()
        
        # Mini progress bar for daily goal (if applicable)
        if stat_type == "study_time":
            progress_frame = tk.Frame(card_frame, bg=color, height=6)
            progress_frame.pack(fill="x", padx=10, pady=(0, 10))
            progress_frame.pack_propagate(False)
            
            # Progress bar background
            progress_bg = tk.Frame(progress_frame, bg="white", height=4)
            progress_bg.pack(fill="x", pady=1)
            
            # Progress bar fill
            progress_fill = tk.Frame(progress_bg, bg="#f1c40f", height=4)
            progress_fill.pack(side="left", fill="y")
            
            # Store reference for updating
            setattr(self, f"today_{stat_type}_progress", progress_fill)
        
        # Store references for updating
        setattr(self, f"today_{stat_type}_label", value_label)
        setattr(self, f"today_{stat_type}_trend", trend_label)
    
    def create_progress_summary(self, parent):
        """Tạo phần tóm tắt tiến độ với progress bars và visual indicators"""
        summary_frame = ttk.LabelFrame(parent, text="📈 Progress Summary", padding="20")
        summary_frame.pack(fill="x", pady=(15, 10))
        
        # Create a grid layout for better organization
        info_grid = tk.Frame(summary_frame, bg='white')
        info_grid.pack(fill="x")
        
        # Efficiency with color-coded progress bar
        efficiency_frame = tk.Frame(info_grid, bg='white')
        efficiency_frame.grid(row=0, column=0, sticky="ew", padx=(0, 20), pady=8, columnspan=2)
        info_grid.grid_columnconfigure(0, weight=1)
        
        # Efficiency label and value
        eff_header = tk.Frame(efficiency_frame, bg='white')
        eff_header.pack(fill="x")
        
        tk.Label(
            eff_header,
            text="⚡ Study Efficiency:",
            font=("Segoe UI", 11, "bold"),
            bg='white',
            fg='#2c3e50'
        ).pack(side="left")
        
        self.efficiency_label = tk.Label(
            eff_header,
            text="Calculating...",
            font=("Segoe UI", 11, "bold"),
            bg='white',
            fg='#27ae60'
        )
        self.efficiency_label.pack(side="left", padx=(10, 0))
        
        # Add efficiency info toggle button
        self.efficiency_toggle_btn = tk.Label(
            eff_header,
            text="?",
            font=("Segoe UI", 9, "bold"),
            bg='#ecf0f1',
            fg='#3498db',
            relief="raised",
            bd=1,
            padx=3,
            pady=1,
            cursor="hand2"
        )
        self.efficiency_toggle_btn.pack(side="left", padx=(5, 0))
        self.efficiency_toggle_btn.bind("<Button-1>", self.toggle_efficiency_info)
        self.efficiency_toggle_btn.bind("<Enter>", self.on_toggle_hover)
        self.efficiency_toggle_btn.bind("<Leave>", self.on_toggle_leave)
        
        # Initially hidden efficiency info panel
        self.efficiency_info_panel = None
        self.efficiency_info_visible = False
        
        # Efficiency progress bar
        eff_progress_frame = tk.Frame(efficiency_frame, bg='#ecf0f1', height=8, relief="flat", bd=1)
        eff_progress_frame.pack(fill="x", pady=(5, 0))
        eff_progress_frame.pack_propagate(False)
        
        self.efficiency_progress = tk.Frame(eff_progress_frame, bg='#27ae60', height=8)
        self.efficiency_progress.pack(side="left", fill="y")
        
        # Session average with mini chart
        avg_frame = tk.Frame(info_grid, bg='white')
        avg_frame.grid(row=1, column=0, sticky="ew", padx=(0, 20), pady=8, columnspan=2)
        
        avg_header = tk.Frame(avg_frame, bg='white')
        avg_header.pack(fill="x")
        
        tk.Label(
            avg_header,
            text="📊 Average per Session:",
            font=("Segoe UI", 11, "bold"),
            bg='white',
            fg='#2c3e50'
        ).pack(side="left")
        
        self.session_avg_label = tk.Label(
            avg_header,
            text="--:--:--",
            font=("Consolas", 11, "bold"),
            bg='white',
            fg='#8e44ad'
        )
        self.session_avg_label.pack(side="left", padx=(10, 0))
        
        # Mini ASCII chart for session trend
        self.session_chart_label = tk.Label(
            avg_frame,
            text="📈 ▁▂▃▅▆▇█",
            font=("Consolas", 10),
            bg='white',
            fg='#3498db'
        )
        self.session_chart_label.pack(pady=(3, 0))
        
        # Daily Goal with enhanced progress bar
        goal_frame = tk.Frame(info_grid, bg='white')
        goal_frame.grid(row=2, column=0, sticky="ew", padx=(0, 20), pady=8, columnspan=2)
        
        goal_header = tk.Frame(goal_frame, bg='white')
        goal_header.pack(fill="x")
        
        self.goal_title_label = tk.Label(
            goal_header,
            text="🎯 Daily Goal (Auto):",
            font=("Segoe UI", 11, "bold"),
            bg='white',
            fg='#2c3e50'
        )
        self.goal_title_label.pack(side="left")
        
        self.goal_label = tk.Label(
            goal_header,
            text="--",
            font=("Segoe UI", 11, "bold"),
            bg='white',
            fg='#e74c3c'
        )
        self.goal_label.pack(side="left", padx=(10, 0))
        
        # Enhanced progress bar for daily goal
        goal_progress_container = tk.Frame(goal_frame, bg='white')
        goal_progress_container.pack(fill="x", pady=(5, 0))
        
        self.goal_progress_frame = tk.Frame(goal_progress_container, bg='#ecf0f1', height=12, relief="flat", bd=1)
        self.goal_progress_frame.pack(fill="x")
        self.goal_progress_frame.pack_propagate(False)
        
        self.goal_progress_bar = tk.Frame(self.goal_progress_frame, bg='#3498db', height=12)
        self.goal_progress_bar.pack(side="left", fill="y")
        
        # Goal percentage label
        self.goal_percentage_label = tk.Label(
            goal_progress_container,
            text="0%",
            font=("Segoe UI", 9),
            bg='white',
            fg='#7f8c8d'
        )
        self.goal_percentage_label.pack(pady=(2, 0))
    
    def create_weekly_tab(self):
        """Tạo tab thống kê tuần"""
        weekly_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(weekly_frame, text="📊 Weekly")
        
        # Weekly summary cards
        weekly_stats_frame = tk.Frame(weekly_frame, bg='white')
        weekly_stats_frame.pack(fill="x", pady=(0, 20))
        
        # Total study time
        self.create_weekly_card(weekly_stats_frame, "📚 Total Study", "weekly_study", "#2ecc71", 0, 0)
        
        # Active days
        self.create_weekly_card(weekly_stats_frame, "📅 Active Days", "weekly_days", "#3498db", 0, 1)
        
        # Daily average
        self.create_weekly_card(weekly_stats_frame, "📊 Daily Average", "weekly_avg", "#9b59b6", 0, 2)
        
        # Weekly details table
        self.create_weekly_table(weekly_frame)
    
    def create_weekly_card(self, parent, title, stat_type, color, row, col):
        """Tạo card thống kê tuần"""
        card_frame = tk.Frame(parent, bg=color, relief="raised", bd=2)
        card_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew", ipadx=15, ipady=10)
        
        parent.grid_columnconfigure(col, weight=1)
        
        title_label = tk.Label(
            card_frame,
            text=title,
            font=("Arial", 10, "bold"),
            bg=color,
            fg="white"
        )
        title_label.pack()
        
        value_label = tk.Label(
            card_frame,
            text="--",
            font=("Courier New", 14, "bold"),
            bg=color,
            fg="white"
        )
        value_label.pack()
        
        setattr(self, f"{stat_type}_label", value_label)
    
    def create_weekly_table(self, parent):
        """Tạo bảng chi tiết tuần với thiết kế đẹp hơn"""
        table_frame = ttk.LabelFrame(parent, text="📋 Daily Breakdown (Last 7 Days)", padding="15")
        table_frame.pack(fill="both", expand=True)
        
        # Create treeview with better styling
        columns = ("Date", "Study Time", "Break Time", "Sessions", "Tasks", "Efficiency")
        self.weekly_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
        
        # Define headings with better formatting
        column_widths = {"Date": 100, "Study Time": 100, "Break Time": 100, "Sessions": 80, "Tasks": 70, "Efficiency": 90}
        
        for col in columns:
            self.weekly_tree.heading(col, text=col)
            self.weekly_tree.column(col, width=column_widths.get(col, 100), anchor="center")
        
        # Configure row colors for better readability
        self.weekly_tree.tag_configure('evenrow', background='#f8f9fa')
        self.weekly_tree.tag_configure('oddrow', background='white')
        self.weekly_tree.tag_configure('today', background='#e3f2fd', foreground='#1565c0')
        self.weekly_tree.tag_configure('high_productivity', background='#e8f5e8', foreground='#2e7d32')
        
        # Scrollbar with better styling
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.weekly_tree.yview)
        self.weekly_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack with better layout
        self.weekly_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind double-click event for date overlay
        self.weekly_tree.bind("<Double-1>", self.on_weekly_double_click)
    
    def create_monthly_tab(self):
        """Tạo tab thống kê tháng"""
        monthly_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(monthly_frame, text="📅 Monthly")
        
        # Month selector
        month_selector_frame = tk.Frame(monthly_frame, bg='white')
        month_selector_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(
            month_selector_frame,
            text="📅 Select Month:",
            font=("Arial", 12, "bold"),
            bg='white'
        ).pack(side="left", padx=(0, 10))
        
        # Month/Year selection
        self.month_var = tk.StringVar()
        self.month_combo = ttk.Combobox(
            month_selector_frame,
            textvariable=self.month_var,
            state="readonly",
            width=15
        )
        self.month_combo.pack(side="left", padx=5)
        self.month_combo.bind("<<ComboboxSelected>>", self.on_month_changed)
        
        # Populate months (current month + 11 previous months)
        self.populate_month_options()
        
        # Monthly summary cards
        monthly_summary_frame = tk.Frame(monthly_frame, bg='white')
        monthly_summary_frame.pack(fill="x", pady=(0, 15))
        
        # Total study time
        self.create_monthly_card(monthly_summary_frame, "📚 Total Study", "monthly_study", "#27ae60", 0, 0)
        
        # Active days
        self.create_monthly_card(monthly_summary_frame, "📅 Active Days", "monthly_active", "#3498db", 0, 1)
        
        # Productivity rate
        self.create_monthly_card(monthly_summary_frame, "📊 Productivity", "monthly_productivity", "#e67e22", 0, 2)
        
        # Average daily
        self.create_monthly_card(monthly_summary_frame, "⚡ Daily Avg", "monthly_avg", "#9b59b6", 0, 3)
        
        # Best days section
        best_days_frame = ttk.LabelFrame(monthly_frame, text="🏆 Top 5 Study Days", padding="10")
        best_days_frame.pack(fill="x", pady=(0, 15))
        
        # Best days list
        self.best_days_tree = ttk.Treeview(
            best_days_frame, 
            columns=("Date", "Study Time", "Sessions", "Tasks"), 
            show="headings", 
            height=5
        )
        
        for col in ["Date", "Study Time", "Sessions", "Tasks"]:
            self.best_days_tree.heading(col, text=col)
            self.best_days_tree.column(col, width=120, anchor="center")
        
        self.best_days_tree.pack(fill="x")
        
        # Month comparison
        comparison_frame = ttk.LabelFrame(monthly_frame, text="📈 3-Month Comparison", padding="10")
        comparison_frame.pack(fill="both", expand=True)
        
        self.comparison_tree = ttk.Treeview(
            comparison_frame,
            columns=("Month", "Study Time", "Active Days", "Sessions", "Tasks", "Productivity"),
            show="headings",
            height=4
        )
        
        for col in ["Month", "Study Time", "Active Days", "Sessions", "Tasks", "Productivity"]:
            self.comparison_tree.heading(col, text=col)
            self.comparison_tree.column(col, width=100, anchor="center")
        
        self.comparison_tree.pack(fill="both", expand=True)
    
    def create_monthly_card(self, parent, title, stat_type, color, row, col):
        """Tạo card thống kê tháng với thiết kế gradient và shadow"""
        # Outer container với shadow effect
        shadow_frame = tk.Frame(parent, bg='#bdc3c7', relief="flat", bd=0)
        shadow_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew", ipadx=2, ipady=2)
        
        # Main card với gradient effect
        card_frame = tk.Frame(shadow_frame, bg=color, relief="flat", bd=0)
        card_frame.pack(fill="both", expand=True)
        
        parent.grid_columnconfigure(col, weight=1)
        
        # Icon and title with better spacing
        header_frame = tk.Frame(card_frame, bg=color)
        header_frame.pack(fill="x", pady=(12, 8))
        
        title_label = tk.Label(
            header_frame,
            text=title,
            font=("Segoe UI", 10, "bold"),
            bg=color,
            fg="white"
        )
        title_label.pack()
        
        # Value with monospace font and better size
        value_label = tk.Label(
            card_frame,
            text="--",
            font=("Consolas", 16, "bold"),
            bg=color,
            fg="white"
        )
        value_label.pack(pady=(0, 12))
        
        setattr(self, f"{stat_type}_label", value_label)
    
    def populate_month_options(self):
        """Tạo danh sách các tháng để chọn"""
        from datetime import datetime, timedelta
        import calendar
        
        options = []
        current_date = datetime.now()
        
        # 12 tháng gần đây
        for i in range(12):
            if current_date.month - i > 0:
                month = current_date.month - i
                year = current_date.year
            else:
                month = 12 + (current_date.month - i)
                year = current_date.year - 1
            
            month_name = calendar.month_name[month]
            options.append(f"{month_name} {year}")
        
        self.month_combo['values'] = options
        self.month_combo.set(options[0])  # Set current month as default
    
    def on_month_changed(self, event=None):
        """Xử lý khi thay đổi tháng"""
        self.refresh_monthly_data()
    
    def refresh_monthly_data(self):
        """Cập nhật dữ liệu tháng"""
        if not hasattr(self, 'month_combo'):
            return
            
        selected = self.month_combo.get()
        if not selected:
            return
        
        # Parse month and year from selection
        parts = selected.split()
        month_name = parts[0]
        year = int(parts[1])
        
        import calendar
        month = list(calendar.month_name).index(month_name)
        
        # Get monthly data
        monthly_data = self.stats_manager.get_monthly_data(year, month)
        
        # Update cards
        self.monthly_study_label.config(text=monthly_data["total_study_time"])
        self.monthly_active_label.config(text=f"{monthly_data['active_days']}/{monthly_data['days_in_month']}")
        self.monthly_productivity_label.config(text=monthly_data["productivity_rate"])
        self.monthly_avg_label.config(text=monthly_data["average_daily_study"])
        
        # Update best days
        self.update_best_days(year, month)
        
        # Update comparison
        self.update_month_comparison()
    
    def update_best_days(self, year, month):
        """Cập nhật danh sách ngày học tốt nhất"""
        # Clear existing items
        for item in self.best_days_tree.get_children():
            self.best_days_tree.delete(item)
        
        best_days = self.stats_manager.get_best_days_in_month(year, month, 5)
        
        for day in best_days:
            self.best_days_tree.insert("", "end", values=(
                day["display_date"],
                day["formatted_study_time"],
                day["sessions_completed"],
                day["tasks_completed"]
            ))
    
    def update_month_comparison(self):
        """Cập nhật bảng so sánh 3 tháng"""
        # Clear existing items
        for item in self.comparison_tree.get_children():
            self.comparison_tree.delete(item)
        
        comparisons = self.stats_manager.get_month_comparison(3)
        
        for comp in comparisons:
            self.comparison_tree.insert("", "end", values=(
                comp["month_name"],
                comp["study_time"],
                comp["active_days"],
                comp["sessions"],
                comp["tasks"],
                comp["productivity_rate"]
            ))

    def create_history_tab(self):
        """Tạo tab lịch sử và biểu đồ"""
        history_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(history_frame, text="📈 Charts")
        
        # Chart header
        chart_label = tk.Label(
            history_frame,
            text="📈 Study Time Trend & Analytics",
            font=("Arial", 14, "bold"),
            bg='white'
        )
        chart_label.pack(pady=(0, 10))
        
        # Create matplotlib charts
        self.create_matplotlib_charts(history_frame)
    
    def create_yearly_tab(self):
        """Tạo tab thống kê theo năm"""
        yearly_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(yearly_frame, text="📅 Yearly Stats")
        
        # Year selector frame
        year_selector_frame = tk.Frame(yearly_frame, bg='white')
        year_selector_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(
            year_selector_frame,
            text="📅 Select Year:",
            font=("Arial", 12, "bold"),
            bg='white'
        ).pack(side="left", padx=(0, 10))
        
        # Year selection
        self.year_var = tk.StringVar()
        self.year_combo = ttk.Combobox(
            year_selector_frame,
            textvariable=self.year_var,
            state="readonly",
            width=10
        )
        self.year_combo.pack(side="left", padx=5)
        self.year_combo.bind("<<ComboboxSelected>>", self.on_year_changed)
        
        # Populate years
        self.populate_year_options()
        
        # Yearly summary cards
        yearly_summary_frame = tk.Frame(yearly_frame, bg='white')
        yearly_summary_frame.pack(fill="x", pady=(0, 15))
        
        # Total study hours
        self.create_yearly_card(yearly_summary_frame, "📚 Total Study", "yearly_study", "#27ae60", 0, 0)
        
        # Active days
        self.create_yearly_card(yearly_summary_frame, "📅 Active Days", "yearly_active", "#3498db", 0, 1)
        
        # Average per month
        self.create_yearly_card(yearly_summary_frame, "📊 Monthly Avg", "yearly_monthly_avg", "#e67e22", 0, 2)
        
        # Total sessions
        self.create_yearly_card(yearly_summary_frame, "🎯 Total Sessions", "yearly_sessions", "#9b59b6", 0, 3)
        
        # Monthly breakdown table
        monthly_frame = ttk.LabelFrame(yearly_frame, text="📋 Monthly Breakdown", padding="15")
        monthly_frame.pack(fill="both", expand=True)
        
        # Create treeview for monthly data
        monthly_columns = ("Month", "Study Time", "Break Time", "Sessions", "Tasks", "Active Days", "Productivity")
        self.yearly_tree = ttk.Treeview(monthly_frame, columns=monthly_columns, show="headings", height=12)
        
        # Define headings
        for col in monthly_columns:
            self.yearly_tree.heading(col, text=col)
            self.yearly_tree.column(col, width=120, anchor="center")
        
        # Configure row colors
        self.yearly_tree.tag_configure('high_month', background='#e8f5e8', foreground='#2e7d32')
        self.yearly_tree.tag_configure('medium_month', background='#fff3e0', foreground='#f57c00')
        self.yearly_tree.tag_configure('low_month', background='#ffebee', foreground='#d32f2f')
        self.yearly_tree.tag_configure('current_month', background='#e3f2fd', foreground='#1565c0')
        
        # Scrollbar
        yearly_scrollbar = ttk.Scrollbar(monthly_frame, orient="vertical", command=self.yearly_tree.yview)
        self.yearly_tree.configure(yscrollcommand=yearly_scrollbar.set)
        
        # Pack
        self.yearly_tree.pack(side="left", fill="both", expand=True)
        yearly_scrollbar.pack(side="right", fill="y")
    
    def create_data_explorer_tab(self):
        """Tạo tab khám phá dữ liệu toàn diện"""
        explorer_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(explorer_frame, text="🔍 Data Explorer")
        
        # Control panel
        control_panel = tk.Frame(explorer_frame, bg='white', relief="raised", bd=1)
        control_panel.pack(fill="x", pady=(0, 15))
        
        # Date range selector
        date_range_frame = tk.Frame(control_panel, bg='white')
        date_range_frame.pack(fill="x", padx=15, pady=10)
        
        tk.Label(
            date_range_frame,
            text="📅 Date Range:",
            font=("Arial", 11, "bold"),
            bg='white'
        ).pack(side="left", padx=(0, 10))
        
        # Quick range buttons
        quick_ranges = [
            ("Last 7 Days", 7),
            ("Last 30 Days", 30),
            ("Last 90 Days", 90),
            ("Last 6 Months", 180),
            ("Last Year", 365),
            ("All Data", None)
        ]
        
        for text, days in quick_ranges:
            btn = tk.Button(
                date_range_frame,
                text=text,
                command=lambda d=days: self.load_data_range(d),
                bg="#3498db",
                fg="white",
                font=("Arial", 9),
                relief="flat",
                padx=10,
                pady=5,
                cursor="hand2"
            )
            btn.pack(side="left", padx=2)
        
        # Custom date range
        custom_range_frame = tk.Frame(control_panel, bg='white')
        custom_range_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        tk.Label(
            custom_range_frame,
            text="🗓️ Custom Range:",
            font=("Arial", 11, "bold"),
            bg='white'
        ).pack(side="left", padx=(0, 10))
        
        tk.Label(custom_range_frame, text="From:", bg='white').pack(side="left", padx=(10, 5))
        self.start_date_var = tk.StringVar()
        self.start_date_entry = tk.Entry(custom_range_frame, textvariable=self.start_date_var, width=12)
        self.start_date_entry.pack(side="left", padx=2)
        
        tk.Label(custom_range_frame, text="To:", bg='white').pack(side="left", padx=(10, 5))
        self.end_date_var = tk.StringVar()
        self.end_date_entry = tk.Entry(custom_range_frame, textvariable=self.end_date_var, width=12)
        self.end_date_entry.pack(side="left", padx=2)
        
        custom_load_btn = tk.Button(
            custom_range_frame,
            text="Load Range",
            command=self.load_custom_range,
            bg="#27ae60",
            fg="white",
            font=("Arial", 9),
            relief="flat",
            padx=15,
            cursor="hand2"
        )
        custom_load_btn.pack(side="left", padx=10)
        
        # Data summary
        summary_frame = tk.Frame(explorer_frame, bg='white', relief="raised", bd=1)
        summary_frame.pack(fill="x", pady=(0, 15))
        
        summary_header = tk.Label(
            summary_frame,
            text="📊 Data Summary",
            font=("Arial", 12, "bold"),
            bg='white',
            fg='#2c3e50'
        )
        summary_header.pack(pady=(10, 5))
        
        self.summary_text = tk.Text(
            summary_frame,
            height=4,
            font=("Consolas", 10),
            bg='#f8f9fa',
            fg='#2c3e50',
            relief="flat",
            wrap="word"
        )
        self.summary_text.pack(fill="x", padx=15, pady=(0, 10))
        
        # Detailed data table
        table_frame = ttk.LabelFrame(explorer_frame, text="📋 Detailed Data", padding="10")
        table_frame.pack(fill="both", expand=True)
        
        # Create treeview for all data
        data_columns = ("Date", "Study Time", "Break Time", "Sessions", "Tasks", "Efficiency", "Goal Progress")
        self.explorer_tree = ttk.Treeview(table_frame, columns=data_columns, show="headings", height=15)
        
        # Define headings with better widths
        column_widths = {
            "Date": 100,
            "Study Time": 100,
            "Break Time": 100,
            "Sessions": 80,
            "Tasks": 70,
            "Efficiency": 90,
            "Goal Progress": 100
        }
        
        for col in data_columns:
            self.explorer_tree.heading(col, text=col)
            self.explorer_tree.column(col, width=column_widths.get(col, 100), anchor="center")
        
        # Configure advanced row colors
        self.explorer_tree.tag_configure('excellent_day', background='#e8f5e8', foreground='#2e7d32')
        self.explorer_tree.tag_configure('great_day', background='#f3e5f5', foreground='#7b1fa2')
        self.explorer_tree.tag_configure('good_day', background='#e3f2fd', foreground='#1565c0')
        self.explorer_tree.tag_configure('fair_day', background='#fff3e0', foreground='#f57c00')
        self.explorer_tree.tag_configure('poor_day', background='#ffebee', foreground='#d32f2f')
        self.explorer_tree.tag_configure('no_data', background='#f5f5f5', foreground='#9e9e9e')
        self.explorer_tree.tag_configure('today', background='#fffde7', foreground='#f57f17')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.explorer_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.explorer_tree.xview)
        self.explorer_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack table and scrollbars
        self.explorer_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Bind double-click event for date overlay
        self.explorer_tree.bind("<Double-1>", self.on_explorer_double_click)
        
        # Initialize with last 30 days
        self.load_data_range(30)
    
    def create_control_buttons(self, parent):
        """Tạo các nút điều khiển với thiết kế Material Design"""
        button_frame = tk.Frame(parent, bg='#f5f5f5')
        button_frame.pack(fill="x", pady=(20, 0))
        
        # Button style configuration
        button_config = {
            "font": ("Segoe UI", 10, "bold"),
            "relief": "flat",
            "bd": 0,
            "padx": 20,
            "pady": 12,
            "cursor": "hand2"
        }
        
        # Refresh button with hover effect
        refresh_btn = tk.Button(
            button_frame,
            text="🔄 Refresh Data",
            command=self.refresh_data,
            bg="#3498db",
            fg="white",
            **button_config
        )
        refresh_btn.pack(side="left", padx=(0, 15))
        
        # Reset today button
        reset_btn = tk.Button(
            button_frame,
            text="🗑️ Reset Today",
            command=self.reset_today,
            bg="#e74c3c",
            fg="white",
            **button_config
        )
        reset_btn.pack(side="left", padx=5)
        
        # Export button
        export_btn = tk.Button(
            button_frame,
            text="📤 Export Data",
            command=self.export_data,
            bg="#27ae60",
            fg="white",
            **button_config
        )
        export_btn.pack(side="left", padx=5)
        
        # Export Charts button (only show if matplotlib available)
        if MATPLOTLIB_AVAILABLE:
            export_charts_btn = tk.Button(
                button_frame,
                text="📊 Export Charts",
                command=self.export_charts,
                bg="#9b59b6",
                fg="white",
                **button_config
            )
            export_charts_btn.pack(side="left", padx=5)
        
        # Spacer
        spacer = tk.Frame(button_frame, bg='#f5f5f5')
        spacer.pack(side="left", expand=True, fill="x")
        
        # Close button
        close_btn = tk.Button(
            button_frame,
            text="❌ Close Window",
            command=self.on_close,
            bg="#95a5a6",
            fg="white",
            **button_config
        )
        close_btn.pack(side="right")
    
    def refresh_data(self):
        """Cập nhật dữ liệu hiển thị với trend indicators và visual enhancements"""
        if not self.window:
            return
            
        # Get today's and yesterday's data for comparison
        today_summary = self.stats_manager.get_today_summary()
        recent_days = self.stats_manager.get_recent_days(2)  # Today and yesterday
        
        # Get yesterday's data for trend comparison
        yesterday_data = recent_days[1] if len(recent_days) > 1 else None
        
        # Update today's stats with enhanced display
        self.update_stat_card_with_trend("study_time", today_summary["study_time"], yesterday_data)
        self.update_stat_card_with_trend("break_time", today_summary["break_time"], yesterday_data)
        self.update_stat_card_with_trend("sessions", today_summary["sessions_completed"], yesterday_data)
        self.update_stat_card_with_trend("tasks", today_summary["tasks_completed"], yesterday_data)
        
        # Update progress summary with enhanced visuals
        self.update_progress_summary(today_summary)
        
        # Update motivational message
        study_seconds = self.time_to_seconds(today_summary["study_time"])
        self.update_motivational_section(study_seconds)
        
        # Update achievement badges
        sessions = int(today_summary["sessions_completed"])
        tasks = int(today_summary["tasks_completed"])
        self.update_achievement_section(study_seconds, sessions, tasks)
        
        # Update weekly stats
        weekly_summary = self.stats_manager.get_weekly_total()
        
        self.weekly_study_label.config(text=weekly_summary["total_study_time"])
        self.weekly_days_label.config(text=f"{weekly_summary['days_active']}/7")
        self.weekly_avg_label.config(text=weekly_summary["average_daily_study"])
        
        # Update weekly table with enhanced visuals
        self.update_weekly_table()
        
        # Update monthly data if tab exists
        if hasattr(self, 'month_combo'):
            self.refresh_monthly_data()
        
        # Update yearly data if tab exists
        if hasattr(self, 'year_combo'):
            self.refresh_yearly_data()
        
        # Update data explorer if tab exists
        if hasattr(self, 'explorer_tree'):
            self.refresh_explorer_data()
    
    def update_stat_card_with_trend(self, stat_type, current_value, yesterday_data):
        """Cập nhật stat card với trend indicators và visual enhancements"""
        if not hasattr(self, f"today_{stat_type}_label"):
            return
        
        # Update main value
        value_label = getattr(self, f"today_{stat_type}_label")
        value_label.config(text=current_value)
        
        # Update trend indicator
        if hasattr(self, f"today_{stat_type}_trend"):
            trend_label = getattr(self, f"today_{stat_type}_trend")
            
            if yesterday_data:
                # Get yesterday's value for comparison
                if stat_type == "study_time":
                    yesterday_value = yesterday_data["study_time"]
                    current_seconds = self.time_to_seconds(current_value)
                elif stat_type == "break_time":
                    yesterday_value = yesterday_data["break_time"]
                    current_seconds = self.time_to_seconds(current_value)
                elif stat_type == "sessions":
                    yesterday_value = yesterday_data["sessions_completed"]
                    current_seconds = int(current_value)
                elif stat_type == "tasks":
                    yesterday_value = yesterday_data["tasks_completed"]
                    current_seconds = int(current_value)
                
                # Get trend indicator
                trend_text, trend_color = self.get_trend_indicator(current_seconds, yesterday_value)
                trend_label.config(text=trend_text, fg=trend_color)
            else:
                trend_label.config(text="🆕 First day", fg="#3498db")
        
        # Update progress bar for study time
        if stat_type == "study_time" and hasattr(self, f"today_{stat_type}_progress"):
            progress_bar = getattr(self, f"today_{stat_type}_progress")
            current_seconds = self.time_to_seconds(current_value)
            daily_goal_hours = self.stats_manager.get_dynamic_daily_goal()
            daily_goal = daily_goal_hours * 3600  # Convert to seconds
            
            # Calculate progress percentage
            progress = min((current_seconds / daily_goal) * 100, 100)
            
            # Update progress bar width (scale to container)
            progress_width = int(progress * 2)  # Scale factor
            progress_bar.config(width=max(progress_width, 1))
            
            # Change color based on progress
            if progress >= 100:
                progress_bar.config(bg="#27ae60")  # Green for completed
            elif progress >= 75:
                progress_bar.config(bg="#f1c40f")  # Yellow for almost there
            elif progress >= 50:
                progress_bar.config(bg="#3498db")  # Blue for good progress
            else:
                progress_bar.config(bg="#e74c3c")  # Red for low progress

    def update_session_chart(self):
        """Cập nhật mini chart cho session average"""
        if not hasattr(self, 'session_chart_label'):
            return
        
        # Get last 7 days of session data
        recent_days = self.stats_manager.get_recent_days(7)
        session_values = [day["sessions_completed"] for day in recent_days]
        
        # Create ASCII chart
        chart = self.create_ascii_chart(session_values)
        self.session_chart_label.config(text=f"📈 {chart}")

    def update_efficiency_progress(self, efficiency_percent):
        """Cập nhật progress bar cho efficiency"""
        if not hasattr(self, 'efficiency_progress'):
            return
        
        # Update progress bar width
        progress_width = int(efficiency_percent * 2)  # Scale factor
        self.efficiency_progress.config(width=max(progress_width, 1))
        
        # Change color based on efficiency
        if efficiency_percent >= 80:
            self.efficiency_progress.config(bg="#27ae60")  # Green for excellent
        elif efficiency_percent >= 60:
            self.efficiency_progress.config(bg="#f39c12")  # Orange for good
        elif efficiency_percent >= 40:
            self.efficiency_progress.config(bg="#e67e22")  # Orange-red for fair
        else:
            self.efficiency_progress.config(bg="#e74c3c")  # Red for poor

    def update_goal_progress_visual(self, progress_percent):
        """Cập nhật visual cho daily goal progress"""
        if not hasattr(self, 'goal_progress_bar') or not hasattr(self, 'goal_percentage_label'):
            return
        
        # Update progress bar
        progress_width = int(progress_percent * 3)  # Scale factor
        self.goal_progress_bar.config(width=max(progress_width, 1))
        
        # Update percentage label
        self.goal_percentage_label.config(text=f"{progress_percent:.1f}%")
        
        # Change colors based on progress
        if progress_percent >= 100:
            self.goal_progress_bar.config(bg="#27ae60")  # Green
            self.goal_percentage_label.config(fg="#27ae60")
        elif progress_percent >= 75:
            self.goal_progress_bar.config(bg="#f1c40f")  # Yellow
            self.goal_percentage_label.config(fg="#f39c12")
        elif progress_percent >= 50:
            self.goal_progress_bar.config(bg="#3498db")  # Blue
            self.goal_percentage_label.config(fg="#3498db")
        else:
            self.goal_progress_bar.config(bg="#e74c3c")  # Red
            self.goal_percentage_label.config(fg="#e74c3c")

    def add_motivational_message(self, study_seconds):
        """Thêm motivational message dựa trên thời gian học"""
        if study_seconds >= 4 * 3600:  # 4+ hours
            return "🏆 Outstanding! You're crushing your goals!"
        elif study_seconds >= 3 * 3600:  # 3+ hours
            return "🔥 Excellent work! Almost at your daily goal!"
        elif study_seconds >= 2 * 3600:  # 2+ hours
            return "💪 Great progress! Keep the momentum going!"
        elif study_seconds >= 1 * 3600:  # 1+ hour
            return "⏱️ Good start! You're building the habit!"
        elif study_seconds > 0:
            return "🎯 Every minute counts! Keep going!"
        else:
            return "🚀 Ready to start your learning journey?"

    def create_achievement_badges(self, parent, study_seconds, sessions, tasks):
        """Tạo achievement badges dựa trên thống kê"""
        badge_frame = tk.Frame(parent, bg='white')
        badge_frame.pack(fill="x", pady=(10, 0))
        
        badges = []
        
        # Study time badges
        if study_seconds >= 4 * 3600:
            badges.append("🏆 Goal Master")
        elif study_seconds >= 2 * 3600:
            badges.append("💪 Dedicated")
        elif study_seconds >= 1 * 3600:
            badges.append("⭐ Consistent")
        
        # Session badges
        if sessions >= 8:
            badges.append("🎯 Focus Champion")
        elif sessions >= 4:
            badges.append("📚 Study Warrior")
        
        # Task badges
        if tasks >= 5:
            badges.append("✅ Task Master")
        elif tasks >= 3:
            badges.append("🎪 Productive")
        
        if badges:
            badge_label = tk.Label(
                badge_frame,
                text=" • ".join(badges),
                font=("Segoe UI", 10, "bold"),
                bg='white',
                fg='#2c3e50'
            )
            badge_label.pack()
        
        return badge_frame

    def animate_progress_bar(self, progress_bar, target_width):
        """Tạo hiệu ứng animate cho progress bar"""
        current_width = progress_bar.winfo_width()
        
        def animate_step(current, target, step=0):
            if step >= 10:  # Animation steps
                return
            
            new_width = current + (target - current) * (step + 1) / 10
            progress_bar.config(width=int(new_width))
            
            # Schedule next step
            self.window.after(50, lambda: animate_step(current, target, step + 1))
        
        animate_step(current_width, target_width)

    def create_motivational_section(self, parent):
        """Tạo phần motivational message"""
        self.motivational_frame = tk.Frame(parent, bg='white', relief="raised", bd=1)
        self.motivational_frame.pack(fill="x", pady=(15, 10), padx=20)
        
        # Header
        header_label = tk.Label(
            self.motivational_frame,
            text="💝 Today's Motivation",
            font=("Segoe UI", 12, "bold"),
            bg='white',
            fg='#2c3e50'
        )
        header_label.pack(pady=(10, 5))
        
        # Motivational message
        self.motivational_label = tk.Label(
            self.motivational_frame,
            text="🚀 Ready to start your learning journey?",
            font=("Segoe UI", 11, "italic"),
            bg='white',
            fg='#3498db',
            wraplength=400
        )
        self.motivational_label.pack(pady=(0, 10))

    def create_achievement_section(self, parent):
        """Tạo phần achievement badges"""
        self.achievement_frame = tk.Frame(parent, bg='white', relief="raised", bd=1)
        self.achievement_frame.pack(fill="x", pady=(10, 0), padx=20)
        
        # Header
        header_label = tk.Label(
            self.achievement_frame,
            text="🏆 Today's Achievements",
            font=("Segoe UI", 12, "bold"),
            bg='white',
            fg='#2c3e50'
        )
        header_label.pack(pady=(10, 5))
        
        # Achievement badges container
        self.achievement_badges_frame = tk.Frame(self.achievement_frame, bg='white')
        self.achievement_badges_frame.pack(fill="x", pady=(0, 10), padx=10)
        
        # Initial empty message
        self.achievement_label = tk.Label(
            self.achievement_badges_frame,
            text="🎯 Start studying to unlock achievements!",
            font=("Segoe UI", 10),
            bg='white',
            fg='#7f8c8d'
        )
        self.achievement_label.pack()

    def update_motivational_section(self, study_seconds):
        """Cập nhật motivational message"""
        if hasattr(self, 'motivational_label'):
            message = self.add_motivational_message(study_seconds)
            self.motivational_label.config(text=message)

    def update_achievement_section(self, study_seconds, sessions, tasks):
        """Cập nhật achievement badges"""
        if not hasattr(self, 'achievement_badges_frame'):
            return
        
        # Clear existing badges
        for widget in self.achievement_badges_frame.winfo_children():
            widget.destroy()
        
        badges = []
        
        # Study time badges
        if study_seconds >= 4 * 3600:
            badges.append("🏆 Goal Master")
        elif study_seconds >= 3 * 3600:
            badges.append("🔥 Almost There")
        elif study_seconds >= 2 * 3600:
            badges.append("💪 Dedicated")
        elif study_seconds >= 1 * 3600:
            badges.append("⭐ Consistent")
        
        # Session badges
        if sessions >= 8:
            badges.append("🎯 Focus Champion")
        elif sessions >= 6:
            badges.append("📚 Study Warrior")
        elif sessions >= 4:
            badges.append("⚡ Productive")
        
        # Task badges
        if tasks >= 10:
            badges.append("✅ Task Master")
        elif tasks >= 5:
            badges.append("🎪 Achiever")
        elif tasks >= 3:
            badges.append("🎨 Getting Things Done")
        
        if badges:
            # Create badges with nice styling
            for i, badge in enumerate(badges):
                badge_label = tk.Label(
                    self.achievement_badges_frame,
                    text=badge,
                    font=("Segoe UI", 10, "bold"),
                    bg='#3498db',
                    fg='white',
                    relief="raised",
                    bd=2,
                    padx=10,
                    pady=5
                )
                badge_label.pack(side="left", padx=5, pady=2)
        else:
            # Show encouragement message
            self.achievement_label = tk.Label(
                self.achievement_badges_frame,
                text="🎯 Start studying to unlock achievements!",
                font=("Segoe UI", 10),
                bg='white',
                fg='#7f8c8d'
            )
            self.achievement_label.pack()

    def update_progress_summary(self, today_summary):
        """Cập nhật phần tóm tắt tiến độ với màu sắc và visual cues"""
        # Calculate efficiency (study time vs total time)
        study_seconds = self.time_to_seconds(today_summary["study_time"])
        break_seconds = self.time_to_seconds(today_summary["break_time"])
        total_seconds = study_seconds + break_seconds
        
        if total_seconds > 0:
            efficiency = (study_seconds / total_seconds) * 100
            # Color code efficiency
            if efficiency >= 80:
                color = '#27ae60'  # Green for excellent
                emoji = "🔥"
            elif efficiency >= 60:
                color = '#f39c12'  # Orange for good
                emoji = "💪"
            else:
                color = '#e74c3c'  # Red for needs improvement
                emoji = "📈"
            
            self.efficiency_label.config(text=f"{efficiency:.1f}% {emoji}", fg=color)
            
            # Update efficiency progress bar
            self.update_efficiency_progress(efficiency)
        else:
            self.efficiency_label.config(text="-- 🎯", fg='#95a5a6')
            if hasattr(self, 'efficiency_progress'):
                self.efficiency_progress.config(width=1, bg='#95a5a6')
        
        # Average per session with enhanced display
        sessions = int(today_summary["sessions_completed"])
        if sessions > 0:
            avg_per_session = study_seconds // sessions
            avg_formatted = self.stats_manager.format_time(avg_per_session)
            
            # Add visual indicator for session quality
            if avg_per_session >= 1800:  # 30+ minutes
                avg_display = f"{avg_formatted} 🔥"
            elif avg_per_session >= 1200:  # 20+ minutes
                avg_display = f"{avg_formatted} 💪"
            else:
                avg_display = f"{avg_formatted} ⏱️"
            
            self.session_avg_label.config(text=avg_display)
        else:
            self.session_avg_label.config(text="--:--:-- 🎯")
        
        # Update session chart
        self.update_session_chart()
        
        # Daily goal with enhanced visual progress (dynamic)
        daily_goal_hours = self.stats_manager.get_dynamic_daily_goal()
        daily_goal_seconds = daily_goal_hours * 3600
        
        # Update goal title with current goal
        self.goal_title_label.config(text=f"🎯 Daily Goal ({daily_goal_hours:.1f}h):")
        
        if study_seconds > 0:
            goal_progress = min((study_seconds / daily_goal_seconds) * 100, 100)
            
            # Color code goal progress with enhanced messaging
            if goal_progress >= 100:
                goal_color = '#27ae60'  # Green for completed
                goal_text = f"{goal_progress:.1f}% ✅ Goal Achieved!"
            elif goal_progress >= 75:
                goal_color = '#f39c12'  # Orange for almost there
                goal_text = f"{goal_progress:.1f}% 🔥 Almost There!"
            elif goal_progress >= 50:
                goal_color = '#3498db'  # Blue for good progress
                goal_text = f"{goal_progress:.1f}% 💪 Good Progress"
            elif goal_progress >= 25:
                goal_color = '#e67e22'  # Orange-red for fair
                goal_text = f"{goal_progress:.1f}% 📈 Keep Going"
            else:
                goal_color = '#e74c3c'  # Red for low progress
                goal_text = f"{goal_progress:.1f}% 🎯 Getting Started"
            
            self.goal_label.config(text=goal_text, fg=goal_color)
            
            # Update enhanced progress bar
            self.update_goal_progress_visual(goal_progress)
        else:
            self.goal_label.config(text="0% 🎯 Start Studying", fg='#95a5a6')
            self.update_goal_progress_visual(0)

    def update_weekly_table(self):
        """Cập nhật bảng thống kê tuần với màu sắc và visual indicators"""
        # Clear existing items
        for item in self.weekly_tree.get_children():
            self.weekly_tree.delete(item)
        
        # Get recent days data
        recent_days = self.stats_manager.get_recent_days(7)
        today_key = self.stats_manager.get_today_key()
        
        for i, day in enumerate(recent_days):
            # Format date nicely
            date_obj = datetime.strptime(day["date"], "%Y-%m-%d")
            formatted_date = date_obj.strftime("%m/%d (%a)")
            
            # Calculate efficiency for this day
            study_time = day["study_time"]
            break_time = day["break_time"]
            total_time = study_time + break_time
            
            if total_time > 0:
                efficiency = (study_time / total_time) * 100
                efficiency_text = f"{efficiency:.0f}%"
            else:
                efficiency_text = "--"
            
            # Determine row styling
            if day["date"] == today_key:
                tag = 'today'
            elif study_time >= 2 * 3600:  # 2+ hours = high productivity
                tag = 'high_productivity'
            elif i % 2 == 0:
                tag = 'evenrow'
            else:
                tag = 'oddrow'
            
            # Add visual indicators to study time
            study_display = day["formatted_study_time"]
            if study_time >= 4 * 3600:  # 4+ hours
                study_display += " 🔥"
            elif study_time >= 2 * 3600:  # 2+ hours
                study_display += " 💪"
            elif study_time > 0:
                study_display += " ⏱️"
            
            self.weekly_tree.insert("", "end", values=(
                formatted_date,
                study_display,
                day["formatted_break_time"],
                f"{day['sessions_completed']} 🎯" if day['sessions_completed'] > 0 else "0",
                f"{day['tasks_completed']} ✅" if day['tasks_completed'] > 0 else "0",
                efficiency_text
            ), tags=(tag,))

    def time_to_seconds(self, time_str):
        """Chuyển đổi thời gian HH:MM:SS thành giây"""
        try:
            parts = time_str.split(":")
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        except:
            return 0

    def reset_today(self):
        """Reset thống kê ngày hôm nay"""
        confirm = messagebox.askyesno(
            "Reset Today's Statistics",
            "Are you sure you want to reset today's statistics?\n\n"
            "This will clear:\n"
            "• Study time\n"
            "• Break time\n"
            "• Sessions completed\n"
            "• Tasks completed\n\n"
            "This action cannot be undone.",
            icon='warning'
        )
        
        if confirm:
            self.stats_manager.reset_today()
            self.refresh_data()
            messagebox.showinfo("Reset Complete", "Today's statistics have been reset.")

    def export_data(self):
        """Xuất dữ liệu thống kê"""
        from tkinter import filedialog
        
        filename = filedialog.asksaveasfilename(
            title="Export Statistics",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                import shutil
                shutil.copy(self.stats_manager.stats_file, filename)
                messagebox.showinfo("Export Successful", f"Statistics exported to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Export Failed", f"Could not export data:\n{e}")

    def export_charts(self):
        """Xuất biểu đồ thành file hình ảnh với thiết kế đẹp"""
        if not MATPLOTLIB_AVAILABLE:
            messagebox.showwarning("Export Charts", "Matplotlib is required to export charts.\nPlease install it with: pip install matplotlib")
            return
        
        from tkinter import filedialog
        import os
        
        # Chọn thư mục để lưu
        folder = filedialog.askdirectory(title="Choose folder to save charts")
        if not folder:
            return
        
        try:
            # Get data
            recent_days = self.stats_manager.get_recent_days(14)
            if not recent_days:
                messagebox.showwarning("Export Charts", "No data available to export.")
                return
            
            # Prepare data
            dates = []
            study_hours = []
            break_hours = []
            sessions = []
            tasks = []
            efficiency_values = []
            goal_progress = []
            
            for day in recent_days:
                date_obj = datetime.strptime(day["date"], "%Y-%m-%d")
                dates.append(date_obj)
                study_hours.append(day["study_time"] / 3600)
                break_hours.append(day["break_time"] / 3600)
                sessions.append(day["sessions_completed"])
                tasks.append(day["tasks_completed"])
                
                # Calculate efficiency
                study_time = day["study_time"]
                break_time = day["break_time"] 
                total_time = study_time + break_time
                if total_time > 0:
                    efficiency = (study_time / total_time) * 100
                else:
                    efficiency = 0
                efficiency_values.append(efficiency)
                
                # Calculate goal progress (dynamic)
                day_date = datetime.strptime(day["date"], "%Y-%m-%d").date()
                daily_goal_hours = self.stats_manager.get_dynamic_daily_goal(day_date)
                daily_goal_seconds = daily_goal_hours * 3600
                progress = min((study_time / daily_goal_seconds) * 100, 100)
                goal_progress.append(progress)
            
            # 1. Create and save enhanced study time chart
            plt.style.use('default')
            fig, ax = plt.subplots(figsize=(14, 8), dpi=300, facecolor='white')
            ax.set_facecolor('#fafbfc')
            
            # Plot study time with beautiful styling
            ax.plot(dates, study_hours, marker='o', linewidth=3, markersize=8, 
                   color='#2ecc71', label='📚 Study Time', alpha=0.9,
                   markerfacecolor='#27ae60', markeredgecolor='white', markeredgewidth=2)
            ax.fill_between(dates, study_hours, alpha=0.2, color='#2ecc71')
            
            # Plot break time
            ax.plot(dates, break_hours, marker='s', linewidth=2.5, markersize=6,
                   color='#e67e22', label='☕ Break Time', alpha=0.8,
                   markerfacecolor='#d35400', markeredgecolor='white', markeredgewidth=1.5)
            
            # Add daily goal line (dynamic average)
            daily_goal = self.stats_manager.get_dynamic_daily_goal()
            ax.axhline(y=daily_goal, color='#3498db', linestyle='--', linewidth=2, 
                      alpha=0.7, label=f'🎯 Monthly Avg Goal ({daily_goal:.1f}h)')
            
            # Beautiful styling
            ax.set_title('📈 Study Time & Break Analysis (Last 14 Days)', 
                        fontsize=18, fontweight='bold', pad=25, color='#2c3e50')
            ax.set_xlabel('Date', fontsize=14, color='#34495e', fontweight='500')
            ax.set_ylabel('Hours', fontsize=14, color='#34495e', fontweight='500')
            ax.grid(True, alpha=0.4, linestyle='-', linewidth=0.5, color='#bdc3c7')
            ax.set_axisbelow(True)
            
            # Enhanced legend
            legend = ax.legend(loc='upper left', frameon=True, fancybox=True, 
                              shadow=True, fontsize=12, facecolor='white', 
                              edgecolor='#bdc3c7', framealpha=0.95)
            legend.get_frame().set_linewidth(1)
            
            # Format axes
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=35, ha='right', 
                    fontsize=12, color='#5d6d7e')
            plt.setp(ax.yaxis.get_majorticklabels(), fontsize=12, color='#5d6d7e')
            
            # Style borders
            for spine in ax.spines.values():
                spine.set_color('#d5dbdb')
                spine.set_linewidth(1)
            
            plt.tight_layout(pad=2.0)
            plt.savefig(os.path.join(folder, 'study_time_trend.png'), 
                       dpi=300, bbox_inches='tight', facecolor='white')
            plt.close()
            
            # 2. Create and save enhanced sessions & tasks chart
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), dpi=300, facecolor='white')
            
            # Sessions chart
            ax1.set_facecolor('#fafbfc')
            bars1 = ax1.bar(dates, sessions, color='#9b59b6', alpha=0.8, 
                           edgecolor='#8e44ad', linewidth=1.5, capsize=4)
            
            # Add value labels on bars
            for bar in bars1:
                height = bar.get_height()
                if height > 0:
                    ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                            f'{int(height)}', ha='center', va='bottom', 
                            fontsize=11, fontweight='bold', color='#2c3e50',
                            bbox=dict(boxstyle="round,pad=0.3", facecolor='white', 
                                    alpha=0.8, edgecolor='#bdc3c7'))
            
            ax1.set_title('🎯 Daily Sessions Completed', fontsize=16, fontweight='bold', 
                         pad=15, color='#2c3e50')
            ax1.set_ylabel('Sessions', fontsize=12, color='#34495e', fontweight='500')
            ax1.grid(True, alpha=0.4, axis='y', linestyle='-', linewidth=0.5, color='#bdc3c7')
            ax1.set_axisbelow(True)
            
            # Tasks chart
            ax2.set_facecolor('#fafbfc')
            bars2 = ax2.bar(dates, tasks, color='#e74c3c', alpha=0.8,
                           edgecolor='#c0392b', linewidth=1.5, capsize=4)
            
            # Add value labels on bars
            for bar in bars2:
                height = bar.get_height()
                if height > 0:
                    ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                            f'{int(height)}', ha='center', va='bottom', 
                            fontsize=11, fontweight='bold', color='#2c3e50',
                            bbox=dict(boxstyle="round,pad=0.3", facecolor='white', 
                                    alpha=0.8, edgecolor='#bdc3c7'))
            
            ax2.set_title('✅ Daily Tasks Completed', fontsize=16, fontweight='bold', 
                         pad=15, color='#2c3e50')
            ax2.set_xlabel('Date', fontsize=12, color='#34495e', fontweight='500')
            ax2.set_ylabel('Tasks', fontsize=12, color='#34495e', fontweight='500')
            ax2.grid(True, alpha=0.4, axis='y', linestyle='-', linewidth=0.5, color='#bdc3c7')
            ax2.set_axisbelow(True)
            
            # Format axes for both charts
            for ax in [ax1, ax2]:
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
                ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=35, ha='right',
                        fontsize=11, color='#5d6d7e')
                plt.setp(ax.yaxis.get_majorticklabels(), fontsize=11, color='#5d6d7e')
                
                for spine in ax.spines.values():
                    spine.set_color('#d5dbdb')
                    spine.set_linewidth(1)
            
            plt.tight_layout(pad=2.0)
            plt.savefig(os.path.join(folder, 'sessions_tasks_completed.png'), 
                       dpi=300, bbox_inches='tight', facecolor='white')
            plt.close()
            
            # 3. Create and save enhanced efficiency chart
            fig, ax = plt.subplots(figsize=(14, 8), dpi=300, facecolor='white')
            ax.set_facecolor('#fafbfc')
            
            # Plot efficiency
            line1 = ax.plot(dates, efficiency_values, marker='o', linewidth=3, markersize=8,
                           color='#1abc9c', label='⚡ Study Efficiency (%)', alpha=0.9,
                           markerfacecolor='#16a085', markeredgecolor='white', markeredgewidth=2)
            ax.fill_between(dates, efficiency_values, alpha=0.2, color='#1abc9c')
            
            # Create second y-axis for goal progress
            ax2 = ax.twinx()
            ax2.set_facecolor('transparent')
            line2 = ax2.plot(dates, goal_progress, marker='D', linewidth=2.5, markersize=6,
                            color='#3498db', label='🎯 Goal Progress (%)', alpha=0.8,
                            markerfacecolor='#2980b9', markeredgecolor='white', markeredgewidth=1.5)
            
            # Beautiful styling
            ax.set_title('⚡ Study Efficiency & Goal Achievement Analysis', 
                        fontsize=18, fontweight='bold', pad=25, color='#2c3e50')
            ax.set_xlabel('Date', fontsize=14, color='#34495e', fontweight='500')
            ax.set_ylabel('Efficiency (%)', fontsize=14, color='#16a085', fontweight='600')
            ax2.set_ylabel('Goal Progress (%)', fontsize=14, color='#2980b9', fontweight='600')
            
            # Set limits
            ax.set_ylim(0, 105)
            ax2.set_ylim(0, 105)
            
            # Grid and reference lines
            ax.grid(True, alpha=0.4, linestyle='-', linewidth=0.5, color='#bdc3c7')
            ax.set_axisbelow(True)
            
            excellent_line = ax.axhline(y=80, color='#27ae60', linestyle='--', 
                                       linewidth=2, alpha=0.6, label='💪 Excellent (80%)')
            goal_line = ax2.axhline(y=100, color='#e74c3c', linestyle='--', 
                                   linewidth=2, alpha=0.6, label='🏆 Goal Achievement (100%)')
            
            # Enhanced legend
            lines = line1 + line2 + [excellent_line, goal_line]
            labels = [l.get_label() for l in lines]
            legend = ax.legend(lines, labels, loc='upper left', frameon=True, 
                              fancybox=True, shadow=True, fontsize=11,
                              facecolor='white', edgecolor='#bdc3c7', framealpha=0.95)
            legend.get_frame().set_linewidth(1)
            
            # Format axes
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=35, ha='right',
                    fontsize=12, color='#5d6d7e')
            plt.setp(ax.yaxis.get_majorticklabels(), fontsize=12, color='#16a085')
            plt.setp(ax2.yaxis.get_majorticklabels(), fontsize=12, color='#2980b9')
            
            # Style borders
            for spine in ax.spines.values():
                spine.set_color('#d5dbdb')
                spine.set_linewidth(1)
            for spine in ax2.spines.values():
                spine.set_color('#d5dbdb')
                spine.set_linewidth(1)
            
            # Performance zones
            ax.axhspan(0, 40, alpha=0.05, color='red')
            ax.axhspan(40, 60, alpha=0.05, color='orange') 
            ax.axhspan(60, 80, alpha=0.05, color='yellow')
            ax.axhspan(80, 100, alpha=0.05, color='green')
            
            plt.tight_layout(pad=2.0)
            plt.savefig(os.path.join(folder, 'efficiency_analysis.png'), 
                       dpi=300, bbox_inches='tight', facecolor='white')
            plt.close()
            
            messagebox.showinfo("Export Successful", 
                f"📊 Beautiful charts exported to:\n{folder}\n\n✨ Files created:\n• study_time_trend.png (14×8 @ 300 DPI)\n• sessions_tasks_completed.png (14×10 @ 300 DPI)\n• efficiency_analysis.png (14×8 @ 300 DPI)\n\n🎨 Professional quality for reports and presentations!")
            
        except Exception as e:
            messagebox.showerror("Export Failed", f"Could not export charts:\n{e}")

    def on_close(self):
        """Xử lý khi đóng cửa sổ"""
        # Close overlay if open
        if self.overlay_visible:
            self.hide_date_overlay()
        
        self.window.destroy()
        self.window = None

    def add_visual_indicators(self, text: str, value: int, thresholds: dict) -> str:
        """Thêm visual indicators dựa trên giá trị"""
        if value >= thresholds.get('excellent', float('inf')):
            return f"{text} 🔥"
        elif value >= thresholds.get('good', float('inf')):
            return f"{text} 💪"
        elif value > 0:
            return f"{text} ⏱️"
        else:
            return text

    def format_with_emoji(self, value: int, type_name: str) -> str:
        """Format số liệu với emoji tương ứng"""
        if type_name == "sessions" and value > 0:
            return f"{value} 🎯"
        elif type_name == "tasks" and value > 0:
            return f"{value} ✅"
        elif type_name == "study_hours":
            hours = value // 3600
            if hours >= 4:
                return f"{hours}h 🔥"
            elif hours >= 2:
                return f"{hours}h 💪"
            elif hours > 0:
                return f"{hours}h ⏱️"
        return str(value)

    def create_ascii_chart(self, values, width=8):
        """Tạo biểu đồ ASCII đơn giản từ list các giá trị"""
        if not values or max(values) == 0:
            return "▁" * width
        
        # Normalize values to 0-7 range for different bar heights
        max_val = max(values)
        normalized = [int((v / max_val) * 7) for v in values[-width:]]
        
        # Unicode block characters for different heights
        chars = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
        
        return "".join(chars[val] for val in normalized)

    def get_trend_indicator(self, current, previous):
        """Tạo indicator cho xu hướng thay đổi"""
        if previous == 0:
            return "🆕 New", "#3498db"
        
        change_percent = ((current - previous) / previous) * 100
        
        if change_percent > 20:
            return f"🚀 +{change_percent:.0f}%", "#27ae60"
        elif change_percent > 5:
            return f"📈 +{change_percent:.0f}%", "#2ecc71"
        elif change_percent > -5:
            return f"➡️ {change_percent:+.0f}%", "#f39c12"
        elif change_percent > -20:
            return f"📉 {change_percent:.0f}%", "#e67e22"
        else:
            return f"📉 {change_percent:.0f}%", "#e74c3c"

    def format_time_with_units(self, seconds):
        """Format thời gian với đơn vị rõ ràng"""
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"{minutes}m"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            if minutes == 0:
                return f"{hours}h"
            else:
                return f"{hours}h {minutes}m"

    def create_matplotlib_charts(self, parent):
        """Tạo biểu đồ matplotlib cho data visualization"""
        if not MATPLOTLIB_AVAILABLE:
            # Fallback to placeholder if matplotlib not available
            self.create_chart_placeholder(parent)
            return
        
        try:
            # Create notebook for multiple charts
            chart_notebook = ttk.Notebook(parent)
            chart_notebook.pack(fill="both", expand=True)
            
            # Study Time Trend Chart
            self.create_study_time_chart(chart_notebook)
            
            # Daily Sessions Chart (separate tab)
            self.create_sessions_chart(chart_notebook)
            
            # Daily Tasks Chart (separate tab)
            self.create_tasks_chart(chart_notebook)
            
            # Efficiency and Progress Chart
            self.create_efficiency_chart(chart_notebook)
            
        except Exception as e:
            print(f"Error creating charts: {e}")
            self.create_chart_placeholder(parent)
    
    def create_study_time_chart(self, parent):
        """Tạo biểu đồ thời gian học với thiết kế đẹp"""
        # Create frame for study time chart
        study_frame = ttk.Frame(parent, padding="15")
        parent.add(study_frame, text="📚 Study Time")
        
        # Get last 14 days of data
        recent_days = self.stats_manager.get_recent_days(14)
        
        if not recent_days:
            tk.Label(study_frame, text="No data available", font=("Arial", 12)).pack(expand=True)
            return
        
        # Prepare data
        dates = []
        study_hours = []
        break_hours = []
        
        for day in recent_days:
            date_obj = datetime.strptime(day["date"], "%Y-%m-%d")
            dates.append(date_obj)
            study_hours.append(day["study_time"] / 3600)  # Convert to hours
            break_hours.append(day["break_time"] / 3600)
        
        # Create matplotlib figure with beautiful styling
        plt.style.use('default')  # Reset to clean style
        fig = Figure(figsize=(12, 7), dpi=100, facecolor='#f8f9fa')
        ax = fig.add_subplot(111, facecolor='white')
        
        # Create gradient background for better visual appeal
        ax.set_facecolor('#fafbfc')
        
        # Plot study time with enhanced styling
        study_line = ax.plot(dates, study_hours, 
                           marker='o', linewidth=3, markersize=8, 
                           color='#2ecc71', label='📚 Study Time', 
                           alpha=0.9, markerfacecolor='#27ae60',
                           markeredgecolor='white', markeredgewidth=2,
                           zorder=3)
        
        # Add area fill under study time line for visual impact
        ax.fill_between(dates, study_hours, alpha=0.2, color='#2ecc71', zorder=1)
        
        # Plot break time with contrasting style
        break_line = ax.plot(dates, break_hours, 
                           marker='s', linewidth=2.5, markersize=6,
                           color='#e67e22', label='☕ Break Time', 
                           alpha=0.8, markerfacecolor='#d35400',
                           markeredgecolor='white', markeredgewidth=1.5,
                           zorder=2)
        
        # Add daily goal line with enhanced styling (dynamic)
        daily_goal = self.stats_manager.get_dynamic_daily_goal()
        goal_line = ax.axhline(y=daily_goal, color='#3498db', linestyle='--', 
                              linewidth=2, alpha=0.7, 
                              label=f'🎯 Daily Goal ({daily_goal:.1f}h)')
        
        # Customize chart with beautiful typography
        ax.set_title('📈 Study Time & Break Analysis', 
                    fontsize=16, fontweight='bold', pad=25,
                    color='#2c3e50', fontfamily='monospace')
        ax.set_xlabel('Date', fontsize=12, color='#34495e', fontweight='500')
        ax.set_ylabel('Hours', fontsize=12, color='#34495e', fontweight='500')
        
        # Enhanced grid styling
        ax.grid(True, alpha=0.4, linestyle='-', linewidth=0.5, color='#bdc3c7')
        ax.set_axisbelow(True)  # Grid behind data
        
        # Beautiful legend with shadow
        legend = ax.legend(loc='upper left', frameon=True, fancybox=True, 
                          shadow=True, fontsize=11, 
                          facecolor='white', edgecolor='#bdc3c7',
                          framealpha=0.95, borderpad=1)
        legend.get_frame().set_linewidth(1)
        
        # Format x-axis with better styling
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right', 
                fontsize=11, color='#5d6d7e', fontweight='500')
        
        # Style y-axis
        plt.setp(ax.yaxis.get_majorticklabels(), fontsize=11, color='#5d6d7e', fontweight='500')
        
        # Set better axis limits with more padding
        if max(study_hours) > 0:
            ax.set_ylim(0, max(max(study_hours), daily_goal) * 1.15)
        
        # Remove top and right spines for cleaner look
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Add subtle border
        for spine in ['left', 'bottom']:
            ax.spines[spine].set_color('#d5dbdb')
            ax.spines[spine].set_linewidth(1)
        
        # Adjust layout with better margins
        fig.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.15)
        
        # Tight layout with padding
        fig.tight_layout(pad=2.0)
        
        # Add to tkinter
        canvas = FigureCanvasTkAgg(fig, study_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
    
    def create_sessions_chart(self, parent):
        """Tạo biểu đồ sessions riêng biệt với thiết kế đẹp"""
        # Create frame for sessions chart
        session_frame = ttk.Frame(parent, padding="15")
        parent.add(session_frame, text="🎯 Daily Sessions")
        
        # Get last 14 days of data
        recent_days = self.stats_manager.get_recent_days(14)
        
        if not recent_days:
            tk.Label(session_frame, text="No data available", font=("Arial", 12)).pack(expand=True)
            return
        
        # Prepare data
        dates = []
        sessions = []
        
        for day in recent_days:
            date_obj = datetime.strptime(day["date"], "%Y-%m-%d")
            dates.append(date_obj)
            sessions.append(day["sessions_completed"])
        
        # Create matplotlib figure with beautiful styling for sessions only
        fig = Figure(figsize=(14, 8), dpi=100, facecolor='#f8f9fa')
        ax = fig.add_subplot(111, facecolor='#fafbfc')
        
        # Create bars with optimal width for text spacing
        bars = ax.bar(dates, sessions, 
                     color='#9b59b6', alpha=0.8, 
                     edgecolor='#8e44ad', linewidth=1.5,
                     label='🎯 Sessions', capsize=4, width=0.6)
        
        ax.set_title('🎯 Daily Sessions Completed - Detailed Analysis', 
                    fontsize=16, fontweight='bold', pad=20,
                    color='#2c3e50', fontfamily='monospace')
        ax.set_xlabel('Date', fontsize=12, color='#34495e', fontweight='500')
        ax.set_ylabel('Sessions', fontsize=12, color='#34495e', fontweight='500')
        ax.grid(True, alpha=0.4, axis='y', linestyle='-', linewidth=0.5, color='#bdc3c7')
        ax.set_axisbelow(True)
        
        # Add value labels on bars with better styling and no overlap
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.3,
                        f'{int(height)}', ha='center', va='bottom', 
                        fontsize=12, fontweight='bold', color='#2c3e50',
                        bbox=dict(boxstyle="round,pad=0.5", facecolor='white', 
                                alpha=0.98, edgecolor='#8e44ad', linewidth=1.5),
                        zorder=20)
        
        # Add session target line (dynamic: sessions trung bình tháng + 2)
        target_sessions = self.stats_manager.get_dynamic_session_goal()
        ax.axhline(y=target_sessions, color='#3498db', linestyle='--', 
                  linewidth=2, alpha=0.7, 
                  label=f'🎯 Target ({target_sessions} sessions/day)')
        
        # Set y-axis limits to ensure labels are fully visible
        if sessions:
            max_sessions = max(sessions)
            ax.set_ylim(0, max(max_sessions * 1.4, target_sessions * 1.2))
        
        # Format x-axis with enhanced styling
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right',
                fontsize=11, color='#5d6d7e', fontweight='500')
        plt.setp(ax.yaxis.get_majorticklabels(), fontsize=11, color='#5d6d7e', fontweight='500')
        
        # Style axis borders
        for spine in ax.spines.values():
            spine.set_color('#d5dbdb')
            spine.set_linewidth(1)
        
        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Enhanced legend
        legend = ax.legend(loc='upper left', frameon=True, fancybox=True, 
                          shadow=True, fontsize=11, 
                          facecolor='white', edgecolor='#bdc3c7',
                          framealpha=0.95, borderpad=1)
        legend.get_frame().set_linewidth(1)
        
        # Add session performance zones
        if sessions:
            ax.axhspan(0, 2, alpha=0.05, color='red', zorder=0)  # Low productivity
            ax.axhspan(2, 4, alpha=0.05, color='orange', zorder=0)  # Fair productivity  
            ax.axhspan(4, 6, alpha=0.05, color='yellow', zorder=0)  # Good productivity
            ax.axhspan(6, max(max_sessions * 1.4, target_sessions * 1.2), alpha=0.05, color='green', zorder=0)  # Excellent productivity
        
        # Adjust layout with better margins
        fig.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.15)
        fig.tight_layout(pad=2.0)
        
        # Add to tkinter
        canvas = FigureCanvasTkAgg(fig, session_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
    
    def create_tasks_chart(self, parent):
        """Tạo biểu đồ tasks riêng biệt với thiết kế đẹp"""
        # Create frame for tasks chart
        task_frame = ttk.Frame(parent, padding="15")
        parent.add(task_frame, text="✅ Daily Tasks")
        
        # Get last 14 days of data
        recent_days = self.stats_manager.get_recent_days(14)
        
        if not recent_days:
            tk.Label(task_frame, text="No data available", font=("Arial", 12)).pack(expand=True)
            return
        
        # Prepare data
        dates = []
        tasks = []
        
        for day in recent_days:
            date_obj = datetime.strptime(day["date"], "%Y-%m-%d")
            dates.append(date_obj)
            tasks.append(day["tasks_completed"])
        
        # Create matplotlib figure with beautiful styling for tasks only
        fig = Figure(figsize=(14, 8), dpi=100, facecolor='#f8f9fa')
        ax = fig.add_subplot(111, facecolor='#fafbfc')
        
        # Create bars with optimal width for text spacing
        bars = ax.bar(dates, tasks, 
                     color='#e74c3c', alpha=0.8,
                     edgecolor='#c0392b', linewidth=1.5,
                     label='✅ Tasks', capsize=4, width=0.6)
        
        ax.set_title('✅ Daily Tasks Completed - Detailed Analysis', 
                    fontsize=16, fontweight='bold', pad=20,
                    color='#2c3e50', fontfamily='monospace')
        ax.set_xlabel('Date', fontsize=12, color='#34495e', fontweight='500')
        ax.set_ylabel('Tasks', fontsize=12, color='#34495e', fontweight='500')
        ax.grid(True, alpha=0.4, axis='y', linestyle='-', linewidth=0.5, color='#bdc3c7')
        ax.set_axisbelow(True)
        
        # Add value labels on bars with better styling and no overlap
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.3,
                        f'{int(height)}', ha='center', va='bottom', 
                        fontsize=12, fontweight='bold', color='#2c3e50',
                        bbox=dict(boxstyle="round,pad=0.5", facecolor='white', 
                                alpha=0.98, edgecolor='#c0392b', linewidth=1.5),
                        zorder=20)
        
        # Add task target line (example: 8 tasks per day)
        target_tasks = 8
        ax.axhline(y=target_tasks, color='#27ae60', linestyle='--', 
                  linewidth=2, alpha=0.7, 
                  label=f'✅ Target ({target_tasks} tasks/day)')
        
        # Set y-axis limits to ensure labels are fully visible
        if tasks:
            max_tasks = max(tasks)
            ax.set_ylim(0, max(max_tasks * 1.4, target_tasks * 1.2))
        
        # Format x-axis with enhanced styling
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right',
                fontsize=11, color='#5d6d7e', fontweight='500')
        plt.setp(ax.yaxis.get_majorticklabels(), fontsize=11, color='#5d6d7e', fontweight='500')
        
        # Style axis borders
        for spine in ax.spines.values():
            spine.set_color('#d5dbdb')
            spine.set_linewidth(1)
        
        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Enhanced legend
        legend = ax.legend(loc='upper left', frameon=True, fancybox=True, 
                          shadow=True, fontsize=11, 
                          facecolor='white', edgecolor='#bdc3c7',
                          framealpha=0.95, borderpad=1)
        legend.get_frame().set_linewidth(1)
        
        # Add task performance zones
        if tasks:
            ax.axhspan(0, 3, alpha=0.05, color='red', zorder=0)  # Low productivity
            ax.axhspan(3, 5, alpha=0.05, color='orange', zorder=0)  # Fair productivity  
            ax.axhspan(5, 8, alpha=0.05, color='yellow', zorder=0)  # Good productivity
            ax.axhspan(8, max(max_tasks * 1.4, target_tasks * 1.2), alpha=0.05, color='green', zorder=0)  # Excellent productivity
        
        # Adjust layout with better margins
        fig.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.15)
        fig.tight_layout(pad=2.0)
        
        # Add to tkinter
        canvas = FigureCanvasTkAgg(fig, task_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
    
    def create_efficiency_chart(self, parent):
        """Tạo biểu đồ hiệu suất với thiết kế đẹp"""
        # Create frame for efficiency chart
        efficiency_frame = ttk.Frame(parent, padding="15")
        parent.add(efficiency_frame, text="⚡ Efficiency")
        
        # Get last 14 days of data
        recent_days = self.stats_manager.get_recent_days(14)
        
        if not recent_days:
            tk.Label(efficiency_frame, text="No data available", font=("Arial", 12)).pack(expand=True)
            return
        
        # Prepare data
        dates = []
        efficiency_values = []
        goal_progress = []
        
        for day in recent_days:
            date_obj = datetime.strptime(day["date"], "%Y-%m-%d")
            dates.append(date_obj)
            
            # Calculate efficiency
            study_time = day["study_time"]
            break_time = day["break_time"]
            total_time = study_time + break_time
            
            if total_time > 0:
                efficiency = (study_time / total_time) * 100
            else:
                efficiency = 0
            efficiency_values.append(efficiency)
            
            # Calculate goal progress (dynamic daily goal)
            day_date = datetime.strptime(day["date"], "%Y-%m-%d").date()
            daily_goal_hours = self.stats_manager.get_dynamic_daily_goal(day_date)
            daily_goal_seconds = daily_goal_hours * 3600
            progress = min((study_time / daily_goal_seconds) * 100, 100)
            goal_progress.append(progress)
        
        # Create matplotlib figure with enhanced styling and larger size for better visibility
        fig = Figure(figsize=(14, 8), dpi=100, facecolor='#f8f9fa')
        ax = fig.add_subplot(111, facecolor='#fafbfc')
        
        # Plot efficiency with enhanced styling
        line1 = ax.plot(dates, efficiency_values, 
                       marker='o', linewidth=3, markersize=8,
                       color='#1abc9c', label='⚡ Study Efficiency (%)', 
                       alpha=0.9, markerfacecolor='#16a085',
                       markeredgecolor='white', markeredgewidth=2,
                       zorder=3)
        
        # Add area fill under efficiency line
        ax.fill_between(dates, efficiency_values, alpha=0.2, color='#1abc9c', zorder=1)
        
        # Create second y-axis for goal progress
        ax2 = ax.twinx()
        ax2.patch.set_alpha(0)  # Make background transparent
        
        line2 = ax2.plot(dates, goal_progress, 
                        marker='D', linewidth=2.5, markersize=6,
                        color='#3498db', label='🎯 Goal Progress (%)', 
                        alpha=0.8, markerfacecolor='#2980b9',
                        markeredgecolor='white', markeredgewidth=1.5,
                        zorder=2)
        
        # Customize chart with beautiful typography
        ax.set_title('⚡ Study Efficiency & Goal Achievement Analysis', 
                    fontsize=16, fontweight='bold', pad=25,
                    color='#2c3e50', fontfamily='monospace')
        ax.set_xlabel('Date', fontsize=12, color='#34495e', fontweight='500')
        ax.set_ylabel('Efficiency (%)', fontsize=12, color='#16a085', fontweight='600')
        ax2.set_ylabel('Goal Progress (%)', fontsize=12, color='#2980b9', fontweight='600')
        
        # Set y-axis limits with some padding
        ax.set_ylim(0, 105)
        ax2.set_ylim(0, 105)
        
        # Enhanced grid styling
        ax.grid(True, alpha=0.4, linestyle='-', linewidth=0.5, color='#bdc3c7')
        ax.set_axisbelow(True)
        
        # Add reference lines with better styling
        excellent_line = ax.axhline(y=80, color='#27ae60', linestyle='--', 
                                   linewidth=2, alpha=0.6, 
                                   label='💪 Excellent (80%)')
        goal_line = ax2.axhline(y=100, color='#e74c3c', linestyle='--', 
                               linewidth=2, alpha=0.6,
                               label='🏆 Goal Achievement (100%)')
        
        # Format x-axis with better styling and proper spacing
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right',
                fontsize=11, color='#5d6d7e', fontweight='500')
        
        # Style y-axis labels with better visibility
        plt.setp(ax.yaxis.get_majorticklabels(), fontsize=11, color='#16a085', fontweight='500')
        plt.setp(ax2.yaxis.get_majorticklabels(), fontsize=11, color='#2980b9', fontweight='500')
        
        # Remove top spine for cleaner look
        ax.spines['top'].set_visible(False)
        ax2.spines['top'].set_visible(False)
        
        # Style axis borders with better contrast
        for spine_name in ['left', 'bottom', 'right']:
            if spine_name in ax.spines:
                ax.spines[spine_name].set_color('#d5dbdb')
                ax.spines[spine_name].set_linewidth(1)
        for spine_name in ['right']:
            if spine_name in ax2.spines:
                ax2.spines[spine_name].set_color('#d5dbdb')
                ax2.spines[spine_name].set_linewidth(1)
        
        # Adjust layout with better margins for text visibility
        fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.15)
        
        # Beautiful legend with multiple entries
        lines = line1 + line2 + [excellent_line, goal_line]
        labels = [l.get_label() for l in lines]
        legend = ax.legend(lines, labels, loc='upper left', frameon=True, 
                          fancybox=True, shadow=True, fontsize=11,
                          facecolor='white', edgecolor='#bdc3c7',
                          framealpha=0.95, borderpad=1)
        legend.get_frame().set_linewidth(1)
        
        # Add performance zones with subtle background colors
        ax.axhspan(0, 40, alpha=0.05, color='red', zorder=0)  # Poor zone
        ax.axhspan(40, 60, alpha=0.05, color='orange', zorder=0)  # Fair zone  
        ax.axhspan(60, 80, alpha=0.05, color='yellow', zorder=0)  # Good zone
        ax.axhspan(80, 100, alpha=0.05, color='green', zorder=0)  # Excellent zone
        
        # Tight layout with padding
        fig.tight_layout(pad=2.0)
        
        # Add to tkinter
        canvas = FigureCanvasTkAgg(fig, efficiency_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
    
    def create_chart_placeholder(self, parent):
        """Tạo placeholder khi matplotlib không có sẵn"""
        chart_frame = tk.Frame(parent, bg='white', relief="sunken", bd=1)
        chart_frame.pack(fill="both", expand=True)
        
        placeholder_label = tk.Label(
            chart_frame,
            text="📊 Chart functionality requires matplotlib\n\nTo enable charts:\n1. Run: pip install matplotlib\n2. Restart the application\n\nFeatures:\n• Study time trends\n• Session completion rates\n• Efficiency analysis\n• Goal progress tracking",
            font=("Arial", 12),
            bg='white',
            fg='#7f8c8d',
            justify="center"
        )
        placeholder_label.pack(expand=True)

    # Yearly tab methods
    def create_yearly_card(self, parent, title, stat_type, color, row, col):
        """Tạo card thống kê năm với thiết kế đẹp"""
        card_frame = tk.Frame(parent, bg=color, relief="raised", bd=2)
        card_frame.grid(row=row, column=col, padx=8, pady=8, sticky="nsew", ipadx=12, ipady=8)
        
        parent.grid_columnconfigure(col, weight=1)
        
        title_label = tk.Label(
            card_frame,
            text=title,
            font=("Segoe UI", 10, "bold"),
            bg=color,
            fg="white"
        )
        title_label.pack(pady=(5, 2))
        
        value_label = tk.Label(
            card_frame,
            text="--",
            font=("Consolas", 14, "bold"),
            bg=color,
            fg="white"
        )
        value_label.pack()
        
        setattr(self, f"{stat_type}_label", value_label)

    def populate_year_options(self):
        """Tạo danh sách các năm để chọn"""
        available_years = self.stats_manager.get_available_years()
        
        if not available_years:
            # Nếu chưa có dữ liệu, thêm năm hiện tại
            from datetime import datetime
            available_years = [datetime.now().year]
        
        self.year_combo['values'] = available_years
        self.year_combo.set(available_years[0])  # Set năm mới nhất làm mặc định

    def on_year_changed(self, event=None):
        """Xử lý khi thay đổi năm"""
        self.refresh_yearly_data()

    def refresh_yearly_data(self):
        """Cập nhật dữ liệu năm"""
        if not hasattr(self, 'year_combo'):
            return
            
        selected_year = self.year_combo.get()
        if not selected_year:
            return
        
        try:
            year = int(selected_year)
        except ValueError:
            return
        
        # Get yearly data
        yearly_data = self.stats_manager.get_yearly_data(year)
        
        # Update cards
        self.yearly_study_label.config(text=yearly_data["total_study_time"])
        self.yearly_active_label.config(text=f"{yearly_data['active_days']}/365")
        self.yearly_monthly_avg_label.config(text=f"{yearly_data['study_hours_per_month']:.1f}h")
        self.yearly_sessions_label.config(text=str(yearly_data["total_sessions"]))
        
        # Update monthly breakdown table
        self.update_yearly_table(yearly_data)

    def update_yearly_table(self, yearly_data):
        """Cập nhật bảng thống kê tháng trong năm"""
        # Clear existing items
        for item in self.yearly_tree.get_children():
            self.yearly_tree.delete(item)
        
        current_month = datetime.now().month
        current_year = datetime.now().year
        selected_year = int(self.year_combo.get())
        
        for month_data in yearly_data["monthly_stats"]:
            month = month_data["month"]
            
            # Calculate efficiency for the month
            total_study = self.stats_manager.time_to_seconds(month_data["total_study_time"])
            total_break = self.stats_manager.time_to_seconds(month_data["total_break_time"])
            total_time = total_study + total_break
            
            if total_time > 0:
                efficiency = (total_study / total_time) * 100
                efficiency_text = f"{efficiency:.1f}%"
            else:
                efficiency_text = "--"
            
            # Determine row styling based on study hours
            study_hours = total_study / 3600
            if month == current_month and selected_year == current_year:
                tag = 'current_month'
            elif study_hours >= 80:  # 80+ hours per month = excellent
                tag = 'high_month'
            elif study_hours >= 40:  # 40+ hours per month = medium
                tag = 'medium_month'
            elif study_hours > 0:
                tag = 'low_month'
            else:
                tag = ''
            
            # Add visual indicators
            study_display = month_data["total_study_time"]
            if study_hours >= 80:
                study_display += " 🔥"
            elif study_hours >= 40:
                study_display += " 💪"
            elif study_hours > 0:
                study_display += " ⏱️"
            
            self.yearly_tree.insert("", "end", values=(
                month_data["month_name"],
                study_display,
                month_data["total_break_time"],
                f"{month_data['total_sessions']} 🎯" if month_data['total_sessions'] > 0 else "0",
                f"{month_data['total_tasks']} ✅" if month_data['total_tasks'] > 0 else "0",
                f"{month_data['active_days']}/{month_data['days_in_month']}",
                month_data["productivity_rate"]
            ), tags=(tag,))

    # Data Explorer methods
    def load_data_range(self, days):
        """Load data for specified number of days"""
        if days is None:
            # Load all available data
            data_summary = self.stats_manager.get_data_summary()
            if data_summary["earliest_date"]:
                start_date = data_summary["earliest_date"]
                end_date = data_summary["latest_date"]
                self.current_data = self.stats_manager.get_data_range(start_date, end_date)
            else:
                self.current_data = []
        else:
            self.current_data = self.stats_manager.get_data_range(days=days)
        
        self.update_explorer_display()

    def load_custom_range(self):
        """Load data for custom date range"""
        try:
            start_date = self.start_date_var.get()
            end_date = self.end_date_var.get()
            
            if not start_date or not end_date:
                messagebox.showwarning("Invalid Range", "Please enter both start and end dates in YYYY-MM-DD format.")
                return
            
            # Validate date format
            from datetime import datetime
            start_obj = datetime.strptime(start_date, "%Y-%m-%d")
            end_obj = datetime.strptime(end_date, "%Y-%m-%d")
            
            if start_obj > end_obj:
                messagebox.showwarning("Invalid Range", "Start date must be before end date.")
                return
            
            self.current_data = self.stats_manager.get_data_range(start_date, end_date)
            self.update_explorer_display()
            
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter dates in YYYY-MM-DD format (e.g., 2024-01-15).")

    def update_explorer_display(self):
        """Update the data explorer display"""
        self.update_data_summary()
        self.update_explorer_table()

    def update_data_summary(self):
        """Update data summary text"""
        if not hasattr(self, 'summary_text'):
            return
        
        if not self.current_data:
            summary = "📊 No data available for selected range."
        else:
            total_study = sum(day["study_time"] for day in self.current_data)
            total_sessions = sum(day["sessions_completed"] for day in self.current_data)
            total_tasks = sum(day["tasks_completed"] for day in self.current_data)
            active_days = len([day for day in self.current_data if day["study_time"] > 0])
            
            first_date = self.current_data[0]["date"]
            last_date = self.current_data[-1]["date"]
            
            summary = f"""📊 Summary for {first_date} to {last_date} ({len(self.current_data)} days):
📚 Total Study Time: {self.stats_manager.format_time(total_study)} ({total_study/3600:.1f} hours)
🎯 Total Sessions: {total_sessions} | ✅ Total Tasks: {total_tasks}
📅 Active Days: {active_days}/{len(self.current_data)} ({active_days/len(self.current_data)*100:.1f}%)
⚡ Average per Day: {self.stats_manager.format_time(total_study//len(self.current_data)) if len(self.current_data) > 0 else '00:00:00'}"""
        
        self.summary_text.delete(1.0, "end")
        self.summary_text.insert(1.0, summary)

    def update_explorer_table(self):
        """Update the data explorer table"""
        if not hasattr(self, 'explorer_tree'):
            return
        
        # Clear existing items
        for item in self.explorer_tree.get_children():
            self.explorer_tree.delete(item)
        
        if not self.current_data:
            return
        
        today_key = self.stats_manager.get_today_key()
        
        for day in self.current_data:
            # Calculate efficiency
            study_time = day["study_time"]
            break_time = day["break_time"]
            total_time = study_time + break_time
            
            if total_time > 0:
                efficiency = (study_time / total_time) * 100
                efficiency_text = f"{efficiency:.1f}%"
            else:
                efficiency_text = "--"
            
            # Calculate goal progress (dynamic daily goal)
            day_date = datetime.strptime(day["date"], "%Y-%m-%d").date()
            daily_goal_hours = self.stats_manager.get_dynamic_daily_goal(day_date)
            daily_goal_seconds = daily_goal_hours * 3600
            if study_time > 0:
                goal_progress = min((study_time / daily_goal_seconds) * 100, 100)
                goal_text = f"{goal_progress:.1f}%"
            else:
                goal_text = "--"
            
            # Determine row styling
            study_hours = study_time / 3600
            if day["date"] == today_key:
                tag = 'today'
            elif study_time == 0:
                tag = 'no_data'
            elif study_hours >= 6:  # 6+ hours = excellent
                tag = 'excellent_day'
            elif study_hours >= 4:  # 4+ hours = great
                tag = 'great_day'
            elif study_hours >= 2:  # 2+ hours = good
                tag = 'good_day'
            elif study_hours >= 1:  # 1+ hour = fair
                tag = 'fair_day'
            else:
                tag = 'poor_day'
            
            # Format date nicely
            try:
                date_obj = datetime.strptime(day["date"], "%Y-%m-%d")
                formatted_date = date_obj.strftime("%m/%d (%a)")
            except:
                formatted_date = day["date"]
            
            # Add visual indicators
            study_display = day["formatted_study_time"]
            if study_hours >= 4:
                study_display += " 🔥"
            elif study_hours >= 2:
                study_display += " 💪"
            elif study_time > 0:
                study_display += " ⏱️"
            
            self.explorer_tree.insert("", "end", values=(
                formatted_date,
                study_display,
                day["formatted_break_time"],
                f"{day['sessions_completed']} 🎯" if day['sessions_completed'] > 0 else "0",
                f"{day['tasks_completed']} ✅" if day['tasks_completed'] > 0 else "0",
                efficiency_text,
                goal_text
            ), tags=(tag,))

    def refresh_explorer_data(self):
        """Refresh current data in explorer"""
        if hasattr(self, 'current_data'):
            self.update_explorer_display()
    
    def toggle_efficiency_info(self, event=None):
        """Toggle display/hide efficiency info panel"""
        if self.efficiency_info_visible:
            self.hide_efficiency_info()
        else:
            self.show_efficiency_info_panel()
    
    def show_efficiency_info_panel(self):
        """Show efficiency info panel"""
        if self.efficiency_info_panel:
            return
        
        # Find efficiency_frame to insert panel into it
        efficiency_frame = self.efficiency_toggle_btn.master.master
        
        # Create info panel
        self.efficiency_info_panel = tk.Frame(efficiency_frame, bg='#f8f9fa', relief="solid", bd=1)
        self.efficiency_info_panel.pack(fill="x", pady=(8, 0))
        
        # Header with close icon
        header_frame = tk.Frame(self.efficiency_info_panel, bg='#3498db', height=25)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="📊 Study Efficiency Guide",
            font=("Segoe UI", 9, "bold"),
            bg='#3498db',
            fg='white'
        ).pack(side="left", padx=8, expand=True, anchor="w")
        
        close_btn = tk.Label(
            header_frame,
            text="✕",
            font=("Segoe UI", 8, "bold"),
            bg='#3498db',
            fg='white',
            cursor="hand2",
            padx=5
        )
        close_btn.pack(side="right")
        close_btn.bind("<Button-1>", lambda e: self.hide_efficiency_info())
        
        # Content
        content_frame = tk.Frame(self.efficiency_info_panel, bg='#f8f9fa', padx=10, pady=8)
        content_frame.pack(fill="x")
        
        # Formula
        formula_text = "💡 Formula: Efficiency = (Study Time / Total Time) × 100%"
        tk.Label(
            content_frame,
            text=formula_text,
            font=("Segoe UI", 8),
            bg='#f8f9fa',
            fg='#2c3e50',
            wraplength=400,
            justify="left"
        ).pack(anchor="w", pady=(0, 4))
        
        # Levels
        levels_frame = tk.Frame(content_frame, bg='#f8f9fa')
        levels_frame.pack(fill="x", pady=(0, 4))
        
        levels = [
            ("🔥 85-100%", "Excellent", "#27ae60"),
            ("💪 70-84%", "Very Good", "#f39c12"),
            ("📈 50-69%", "Good", "#e67e22"),
            ("⚠️ <50%", "Needs Improvement", "#e74c3c")
        ]
        
        for i, (range_text, desc, color) in enumerate(levels):
            level_frame = tk.Frame(levels_frame, bg='#f8f9fa')
            level_frame.pack(fill="x")
            
            tk.Label(
                level_frame,
                text=f"{range_text}: {desc}",
                font=("Segoe UI", 8),
                bg='#f8f9fa',
                fg=color,
                anchor="w"
            ).pack(side="left")
        
        # Quick tips
        tips_text = "💡 Tip: 85-90% is ideal. 100% = no breaks (not recommended!)"
        tk.Label(
            content_frame,
            text=tips_text,
            font=("Segoe UI", 8, "italic"),
            bg='#f8f9fa',
            fg='#7f8c8d',
            wraplength=400,
            justify="left"
        ).pack(anchor="w", pady=(4, 0))
        
        # Update toggle button
        self.efficiency_toggle_btn.config(text="×", bg='#e74c3c', fg='white')
        self.efficiency_info_visible = True
    
    def hide_efficiency_info(self):
        """Hide efficiency info panel"""
        if self.efficiency_info_panel:
            self.efficiency_info_panel.destroy()
            self.efficiency_info_panel = None
        
        # Reset toggle button
        self.efficiency_toggle_btn.config(text="?", bg='#ecf0f1', fg='#3498db')
        self.efficiency_info_visible = False
    
    def on_toggle_hover(self, event):
        """Hover effect for toggle button"""
        if self.efficiency_info_visible:
            self.efficiency_toggle_btn.config(bg='#c0392b')
        else:
            self.efficiency_toggle_btn.config(bg='#d5dbdb')
    
    def on_toggle_leave(self, event):
        """Remove hover effect for toggle button"""
        if self.efficiency_info_visible:
            self.efficiency_toggle_btn.config(bg='#e74c3c')
        else:
            self.efficiency_toggle_btn.config(bg='#ecf0f1')

    # === DATE OVERLAY METHODS ===
    
    def on_weekly_double_click(self, event):
        """Handle double-click on weekly table"""
        item = self.weekly_tree.selection()[0] if self.weekly_tree.selection() else None
        if item:
            # Get date from the first column
            date_str = self.weekly_tree.item(item, 'values')[0]
            # Convert from display format (MM/DD) to YYYY-MM-DD
            date_str = self.convert_display_date_to_iso(date_str)
            self.show_date_overlay(date_str)
    
    def on_explorer_double_click(self, event):
        """Handle double-click on explorer table"""
        item = self.explorer_tree.selection()[0] if self.explorer_tree.selection() else None
        if item:
            # Get date from the first column
            date_str = self.explorer_tree.item(item, 'values')[0]
            # Convert from display format to YYYY-MM-DD if needed
            date_str = self.convert_display_date_to_iso(date_str)
            self.show_date_overlay(date_str)
    
    def convert_display_date_to_iso(self, display_date):
        """Convert display date format to ISO format (YYYY-MM-DD)"""
        try:
            from datetime import datetime
            # Try different formats
            for fmt in ['%m/%d', '%Y-%m-%d', '%m/%d (%a)', '%Y-%m-%d (%a)']:
                try:
                    if '(' in display_date:
                        # Remove day name in parentheses
                        display_date = display_date.split(' (')[0]
                    
                    if fmt == '%m/%d':
                        # For MM/DD format, add current year
                        parsed_date = datetime.strptime(display_date, fmt)
                        current_year = datetime.now().year
                        return f"{current_year}-{parsed_date.month:02d}-{parsed_date.day:02d}"
                    else:
                        parsed_date = datetime.strptime(display_date, fmt)
                        return parsed_date.strftime('%Y-%m-%d')
                except ValueError:
                    continue
            
            # If all formats fail, return as is
            return display_date
        except Exception:
            return display_date
    
    def show_date_overlay(self, date_str):
        """Show overlay with date details"""
        if self.overlay_visible:
            self.hide_date_overlay()
            return
        
        # Get stats for the selected date
        date_stats = self.stats_manager.get_date_summary(date_str)
        
        # Create overlay
        self.date_overlay = tk.Toplevel(self.window)
        self.date_overlay.title(f"📊 Details for {date_str}")
        self.date_overlay.geometry("600x500")
        self.date_overlay.configure(bg='#f5f5f5')
        self.date_overlay.resizable(False, False)
        
        # Make it modal
        self.date_overlay.transient(self.window)
        self.date_overlay.grab_set()
        
        # Center the overlay
        self.center_overlay()
        
        # Create content similar to Today tab
        self.create_overlay_content(date_stats)
        
        # Bind close events
        self.date_overlay.protocol("WM_DELETE_WINDOW", self.hide_date_overlay)
        self.date_overlay.bind("<Escape>", lambda e: self.hide_date_overlay())
        
        self.overlay_visible = True
    
    def center_overlay(self):
        """Center the overlay on the parent window"""
        self.date_overlay.update_idletasks()
        
        # Get parent window position and size
        parent_x = self.window.winfo_x()
        parent_y = self.window.winfo_y()
        parent_width = self.window.winfo_width()
        parent_height = self.window.winfo_height()
        
        # Get overlay size
        overlay_width = self.date_overlay.winfo_width()
        overlay_height = self.date_overlay.winfo_height()
        
        # Calculate center position
        x = parent_x + (parent_width - overlay_width) // 2
        y = parent_y + (parent_height - overlay_height) // 2
        
        self.date_overlay.geometry(f"{overlay_width}x{overlay_height}+{x}+{y}")
    
    def create_overlay_content(self, date_stats):
        """Create overlay content similar to Today tab"""
        # Header
        header_frame = tk.Frame(self.date_overlay, bg='#2c3e50', height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Header content
        header_content = tk.Frame(header_frame, bg='#2c3e50')
        header_content.pack(expand=True, fill="both")
        
        # Title
        title_label = tk.Label(
            header_content,
            text=f"📊 Study Statistics",
            font=("Segoe UI", 16, "bold"),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(side="left", padx=20, pady=15)
        
        # Date
        date_label = tk.Label(
            header_content,
            text=f"{date_stats['date']}",
            font=("Segoe UI", 12),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        date_label.pack(side="left", padx=(10, 0), pady=15)
        
        # Close button
        close_btn = tk.Button(
            header_content,
            text="✕",
            command=self.hide_date_overlay,
            bg='#e74c3c',
            fg='white',
            font=("Arial", 14, "bold"),
            relief="flat",
            width=3,
            cursor="hand2"
        )
        close_btn.pack(side="right", padx=20, pady=15)
        
        # Main content
        main_frame = tk.Frame(self.date_overlay, bg='#f5f5f5', padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Stats cards
        cards_frame = tk.Frame(main_frame, bg='#f5f5f5')
        cards_frame.pack(fill="x", pady=(0, 20))
        
        # Create 4 stat cards in 2x2 grid
        self.create_overlay_card(cards_frame, "📚 Study Time", date_stats['study_time'], "#2ecc71", 0, 0)
        self.create_overlay_card(cards_frame, "☕ Break Time", date_stats['break_time'], "#f39c12", 0, 1)
        self.create_overlay_card(cards_frame, "🎯 Sessions", date_stats['sessions_completed'], "#9b59b6", 1, 0)
        self.create_overlay_card(cards_frame, "✅ Tasks", date_stats['tasks_completed'], "#e74c3c", 1, 1)
        
        # Progress summary
        self.create_overlay_summary(main_frame, date_stats)
    
    def create_overlay_card(self, parent, title, value, color, row, col):
        """Create a stat card for overlay"""
        card_frame = tk.Frame(parent, bg=color, relief="flat", bd=0)
        card_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Configure grid weights
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        # Title
        title_label = tk.Label(
            card_frame,
            text=title,
            font=("Segoe UI", 11, "bold"),
            bg=color,
            fg='white'
        )
        title_label.pack(fill="x", pady=10)
        
        # Value
        value_label = tk.Label(
            card_frame,
            text=str(value),
            font=("Segoe UI", 18, "bold"),
            bg=color,
            fg='white'
        )
        value_label.pack(fill="x", pady=(0, 15))
        
        # Make card a bit taller
        card_frame.configure(height=100)
    
    def create_overlay_summary(self, parent, date_stats):
        """Create progress summary for overlay"""
        summary_frame = tk.LabelFrame(parent, text="📈 Progress Summary", font=("Segoe UI", 12, "bold"), bg='#f5f5f5')
        summary_frame.pack(fill="x", pady=(10, 0))
        
        # Calculate efficiency
        study_seconds = self.time_to_seconds(date_stats['study_time'])
        break_seconds = self.time_to_seconds(date_stats['break_time'])
        total_seconds = study_seconds + break_seconds
        
        if total_seconds > 0:
            efficiency = (study_seconds / total_seconds) * 100
            efficiency_text = f"{efficiency:.1f}%"
            if efficiency >= 85:
                efficiency_color = "#2ecc71"
                efficiency_level = "🔥 Excellent"
            elif efficiency >= 70:
                efficiency_color = "#f39c12"
                efficiency_level = "💪 Very Good"
            elif efficiency >= 50:
                efficiency_color = "#e67e22"
                efficiency_level = "📈 Good"
            else:
                efficiency_color = "#e74c3c"
                efficiency_level = "⚠️ Needs Improvement"
        else:
            efficiency_text = "N/A"
            efficiency_color = "#95a5a6"
            efficiency_level = "📊 No Data"
        
        # Efficiency display
        efficiency_frame = tk.Frame(summary_frame, bg='#f5f5f5')
        efficiency_frame.pack(fill="x", padx=15, pady=10)
        
        efficiency_label = tk.Label(
            efficiency_frame,
            text="⚡ Study Efficiency:",
            font=("Segoe UI", 11, "bold"),
            bg='#f5f5f5'
        )
        efficiency_label.pack(side="left")
        
        efficiency_value = tk.Label(
            efficiency_frame,
            text=f"{efficiency_text} - {efficiency_level}",
            font=("Segoe UI", 11, "bold"),
            bg='#f5f5f5',
            fg=efficiency_color
        )
        efficiency_value.pack(side="left", padx=(10, 0))
        
        # Total time
        total_frame = tk.Frame(summary_frame, bg='#f5f5f5')
        total_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        total_label = tk.Label(
            total_frame,
            text="⏰ Total Time:",
            font=("Segoe UI", 11, "bold"),
            bg='#f5f5f5'
        )
        total_label.pack(side="left")
        
        total_value = tk.Label(
            total_frame,
            text=date_stats['total_time'],
            font=("Segoe UI", 11),
            bg='#f5f5f5',
            fg='#2c3e50'
        )
        total_value.pack(side="left", padx=(10, 0))
    
    def time_to_seconds(self, time_str):
        """Convert HH:MM:SS to seconds"""
        try:
            parts = time_str.split(':')
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = int(parts[2])
            return hours * 3600 + minutes * 60 + seconds
        except:
            return 0
    
    def hide_date_overlay(self):
        """Hide the date overlay"""
        if self.date_overlay:
            self.date_overlay.destroy()
            self.date_overlay = None
        self.overlay_visible = False
