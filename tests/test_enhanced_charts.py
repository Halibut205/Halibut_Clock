"""
Test file để kiểm tra biểu đồ matplotlib được cải thiện
"""
import os
import sys
import json
import tkinter as tk
from datetime import datetime, timedelta
from random import randint, uniform

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.managers.daily_stats_manager import DailyStatsManager
from src.ui.daily_stats_window import DailyStatsWindow

def create_enhanced_demo_data():
    """Tạo dữ liệu demo phong phú cho test charts đẹp"""
    demo_data = {}
    
    # Tạo dữ liệu cho 21 ngày (3 tuần)
    for i in range(21):
        date = datetime.now() - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        
        # Tạo dữ liệu realistic với pattern
        base_study = 3.5 + uniform(-1, 1.5)  # 2.5-5 hours base
        if i % 7 < 2:  # Weekend - less study
            study_time = max(1, base_study * 0.6)
        else:  # Weekday - more study
            study_time = base_study
            
        # Add some variance
        study_time *= uniform(0.8, 1.2)
        study_time = max(0.5, min(8, study_time))  # 0.5-8 hours
        
        break_time = study_time * uniform(0.2, 0.4)  # 20-40% break
        
        sessions = randint(3, 8)
        tasks = randint(2, 12)
        
        demo_data[date_str] = {
            "date": date_str,
            "study_time": int(study_time * 3600),  # Convert to seconds
            "break_time": int(break_time * 3600),  # Convert to seconds  
            "sessions_completed": sessions,
            "tasks_completed": tasks,
            "focus_sessions": randint(1, sessions),
            "average_focus": uniform(70, 95),
            "productivity_score": uniform(60, 90)
        }
    
    return demo_data

def test_enhanced_charts():
    """Test enhanced beautiful charts"""
    print("🎨 Testing Enhanced Beautiful Charts...")
    
    # Create test data directory
    test_data_dir = "enhanced_test_data"
    if not os.path.exists(test_data_dir):
        os.makedirs(test_data_dir)
    
    # Create enhanced demo data
    demo_data = create_enhanced_demo_data()
    
    # Write demo data to test file  
    test_stats_file = os.path.join(test_data_dir, "daily_stats.json")
    with open(test_stats_file, 'w', encoding='utf-8') as f:
        json.dump(demo_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Created enhanced test data with {len(demo_data)} days")
    
    # Test the stats manager
    stats_manager = DailyStatsManager(data_folder=test_data_dir)
    recent_days = stats_manager.get_recent_days(14)
    print(f"✅ Loaded {len(recent_days)} recent days for charts")
    
    # Show some data info
    if recent_days:
        total_study = sum(day["study_time"] for day in recent_days) / 3600
        avg_sessions = sum(day["sessions_completed"] for day in recent_days) / len(recent_days)
        avg_tasks = sum(day["tasks_completed"] for day in recent_days) / len(recent_days)
        
        print(f"📊 Data Summary:")
        print(f"   📚 Total study time: {total_study:.1f} hours")
        print(f"   🎯 Average sessions/day: {avg_sessions:.1f}")
        print(f"   ✅ Average tasks/day: {avg_tasks:.1f}")
    
    # Create enhanced test window
    root = tk.Tk()
    root.title("🎨 Enhanced Beautiful Charts Demo")
    root.geometry("400x300")
    root.configure(bg='#2c3e50')
    
    # Create beautiful frame
    main_frame = tk.Frame(root, bg='#2c3e50', padx=30, pady=30)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Title
    title_label = tk.Label(main_frame, 
                          text="📊 Enhanced Charts Demo", 
                          font=("Segoe UI", 18, "bold"),
                          bg='#2c3e50', fg='#ecf0f1')
    title_label.pack(pady=(0, 10))
    
    # Subtitle
    subtitle_label = tk.Label(main_frame, 
                             text="🎨 Beautiful matplotlib visualizations", 
                             font=("Segoe UI", 11),
                             bg='#2c3e50', fg='#bdc3c7')
    subtitle_label.pack(pady=(0, 20))
    
    # Enhanced stats info
    info_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.RAISED, bd=1)
    info_frame.pack(fill=tk.X, pady=(0, 20))
    
    if recent_days:
        info_text = f"📈 {len(recent_days)} days • {total_study:.1f}h study • {avg_sessions:.1f} sessions/day"
        info_label = tk.Label(info_frame, text=info_text, 
                             font=("Segoe UI", 10), bg='#34495e', fg='#ecf0f1', pady=8)
        info_label.pack()
    
    def open_enhanced_stats_window():
        """Mở window với enhanced charts"""
        try:
            stats_window = DailyStatsWindow(root, stats_manager)
            stats_window.show()
            
            # Switch to Charts tab automatically if available
            if hasattr(stats_window, 'notebook') and stats_window.notebook:
                # Find charts tab (usually the last one)
                tab_count = stats_window.notebook.index("end")
                if tab_count > 0:
                    stats_window.notebook.select(tab_count - 1)  # Last tab (Charts)
                    print("🎨 Automatically switched to Charts tab")
            
        except Exception as e:
            print(f"❌ Error opening enhanced stats window: {e}")
            tk.messagebox.showerror("Error", f"Could not open charts window:\n{e}")
    
    # Enhanced button
    open_button = tk.Button(main_frame, 
                           text="🚀 Open Enhanced Charts", 
                           command=open_enhanced_stats_window,
                           font=("Segoe UI", 12, "bold"),
                           bg='#3498db', fg='white',
                           relief=tk.FLAT, bd=0, pady=10,
                           cursor='hand2')
    open_button.pack(fill=tk.X, pady=(0, 10))
    
    # Export test button
    def test_export():
        """Test export functionality"""
        try:
            stats_window = DailyStatsWindow(root, stats_manager)
            stats_window.export_charts()
            print("✅ Export test completed")
        except Exception as e:
            print(f"❌ Export test failed: {e}")
    
    export_button = tk.Button(main_frame, 
                             text="💾 Test Export Charts", 
                             command=test_export,
                             font=("Segoe UI", 11),
                             bg='#27ae60', fg='white',
                             relief=tk.FLAT, bd=0, pady=8,
                             cursor='hand2')
    export_button.pack(fill=tk.X)
    
    # Instructions
    instructions = tk.Label(main_frame, 
                           text="Click buttons to test enhanced charts with beautiful styling", 
                           font=("Segoe UI", 9),
                           bg='#2c3e50', fg='#95a5a6',
                           wraplength=300, justify=tk.CENTER)
    instructions.pack(pady=(15, 0))
    
    print("🎨 Enhanced chart test window created!")
    print("📊 Features to test:")
    print("   • Gradient backgrounds and shadows")
    print("   • Professional color schemes")
    print("   • Enhanced typography and legends")
    print("   • Performance zones and goal lines") 
    print("   • High-quality export functionality")
    
    root.mainloop()

if __name__ == "__main__":
    test_enhanced_charts()
