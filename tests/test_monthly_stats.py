#!/usr/bin/env python3
"""
Test Monthly Statistics Feature
Thử nghiệm tính năng thống kê theo tháng
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.managers.daily_stats_manager import DailyStatsManager
from datetime import datetime, timedelta

def test_monthly_stats():
    """Test các chức năng monthly statistics"""
    print("🧪 Testing Monthly Statistics...")
    
    # Khởi tạo manager
    stats = DailyStatsManager()
    
    # Tạo dữ liệu demo cho tháng này
    print("\n📅 Creating demo data for this month...")
    
    # Thêm dữ liệu cho hôm nay
    stats.update_study_time(7200)  # 2 giờ
    stats.update_break_time(1800)  # 30 phút
    stats.increment_sessions_completed()
    stats.increment_sessions_completed()
    stats.increment_tasks_completed()
    stats.increment_tasks_completed()
    stats.increment_tasks_completed()
    
    # Test monthly data
    print("\n📊 Testing get_monthly_data()...")
    monthly_data = stats.get_monthly_data()
    print(f"Month: {monthly_data['month_name']}")
    print(f"Total study time: {monthly_data['total_study_time']}")
    print(f"Active days: {monthly_data['active_days']}/{monthly_data['days_in_month']}")
    print(f"Productivity rate: {monthly_data['productivity_rate']}")
    
    # Test month comparison
    print("\n📈 Testing get_month_comparison()...")
    comparisons = stats.get_month_comparison(3)
    for comp in comparisons:
        print(f"  {comp['month_name']}: {comp['study_time']} study, {comp['active_days']} active days")
    
    # Test best days
    print("\n🏆 Testing get_best_days_in_month()...")
    best_days = stats.get_best_days_in_month()
    for i, day in enumerate(best_days[:3], 1):
        print(f"  #{i}: {day['display_date']} - {day['formatted_study_time']}")
    
    print("\n✅ Monthly statistics tests completed!")

if __name__ == "__main__":
    test_monthly_stats()
