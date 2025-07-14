"""
Test file để kiểm tra biểu đồ matplotlib trong Daily Stats Window
"""
import os
import sys
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import tkinter as tk
from src.managers.daily_stats_manager import DailyStatsManager
from src.ui.daily_stats_window import DailyStatsWindow

def create_rich_demo_data():
    """Tạo dữ liệu demo phong phú để test charts"""
    # Tạo thư mục test data
    test_data_dir = "test_chart_data"
    if not os.path.exists(test_data_dir):
        os.makedirs(test_data_dir)
    
    stats = DailyStatsManager(stats_file=os.path.join(test_data_dir, "stats.json"))
    
    # Tạo dữ liệu cho 14 ngày qua với xu hướng tăng dần
    from datetime import datetime, timedelta
    
    base_date = datetime.now() - timedelta(days=13)
    
    for i in range(14):
        current_date = base_date + timedelta(days=i)
        date_key = current_date.strftime("%Y-%m-%d")
        
        # Tạo dữ liệu với xu hướng tăng và biến động
        base_study = 1800 + (i * 200)  # Tăng dần từ 30 phút
        variation = (i % 3) * 600  # Biến động
        study_time = base_study + variation
        
        break_time = study_time // 4  # Break time = 25% study time
        sessions = min(1 + (i // 3), 6)  # Tăng dần sessions
        tasks = sessions + (i % 2)  # Tasks liên quan sessions
        
        # Cập nhật dữ liệu cho ngày đó
        stats.data[date_key] = {
            "date": date_key,
            "study_time": study_time,
            "break_time": break_time,
            "sessions_completed": sessions,
            "tasks_completed": tasks,
            "start_time": current_date.isoformat(),
            "last_update": current_date.isoformat()
        }
    
    # Lưu dữ liệu
    stats.save_data()
    
    print("📊 Created rich demo data for chart testing:")
    print(f"   📅 Date range: {base_date.strftime('%Y-%m-%d')} to {datetime.now().strftime('%Y-%m-%d')}")
    print(f"   📚 Study time range: {stats.data[list(stats.data.keys())[0]]['study_time']/3600:.1f}h to {stats.data[list(stats.data.keys())[-1]]['study_time']/3600:.1f}h")
    print(f"   🎯 Sessions range: {stats.data[list(stats.data.keys())[0]]['sessions_completed']} to {stats.data[list(stats.data.keys())[-1]]['sessions_completed']}")
    
    return stats

def test_charts():
    """Test biểu đồ matplotlib"""
    print("🧪 Testing Chart Functionality...")
    
    # Create test data directory
    test_data_dir = "test_data"
    if not os.path.exists(test_data_dir):
        os.makedirs(test_data_dir)
    
    # Create demo data
    demo_data = create_rich_demo_data()
    
    # Write demo data to test file  
    test_stats_file = os.path.join(test_data_dir, "daily_stats.json")
    with open(test_stats_file, 'w', encoding='utf-8') as f:
        json.dump(demo_data.stats_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Created test data with {len(demo_data.stats_data)} days")
    
    # Test the stats manager
    stats = DailyStatsManager(data_folder=test_data_dir)
    recent_days = stats.get_recent_days(14)
    print(f"✅ Loaded {len(recent_days)} recent days")
    
    # Tạo root window
    root = tk.Tk()
    root.title("Chart Test - Enhanced Daily Stats")
    root.geometry("300x200")
    root.configure(bg='#2c3e50')
    
    # Tạo nút để mở stats window với charts
    def open_stats_window():
        stats_window = DailyStatsWindow(root, stats)
        stats_window.show()
        # Automatically switch to Charts tab
        if hasattr(stats_window, 'notebook'):
            stats_window.notebook.select(3)  # Charts tab (index 3)
    
    open_btn = tk.Button(
        root,
        text="📊 Open Charts Demo",
        command=open_stats_window,
        font=("Arial", 12, "bold"),
        bg="#3498db",
        fg="white",
        padx=20,
        pady=10,
        cursor="hand2"
    )
    open_btn.pack(expand=True)
    
    # Info label
    info_label = tk.Label(
        root,
        text="Charts include:\n• Study Time Trends\n• Sessions & Tasks\n• Efficiency Analysis",
        font=("Arial", 10),
        fg="white",
        bg='#2c3e50'
    )
    info_label.pack(pady=(10, 20))
    
    # Cleanup function
    def cleanup():
        import shutil
        try:
            if os.path.exists("test_chart_data"):
                shutil.rmtree("test_chart_data")
                print("🧹 Cleaned up test data")
        except:
            pass
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", cleanup)
    
    print("🚀 Chart test window opened! Click button to see charts.")
    root.mainloop()

if __name__ == "__main__":
    test_charts()
