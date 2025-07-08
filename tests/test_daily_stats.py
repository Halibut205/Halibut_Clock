#!/usr/bin/env python3
"""
Test Daily Stats Feature
Demo thử nghiệm chức năng thống kê hàng ngày
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.managers.daily_stats_manager import DailyStatsManager

def test_daily_stats():
    """Test các chức năng của DailyStatsManager"""
    print("🧪 Testing Daily Stats Manager...")
    
    # Khởi tạo manager
    stats = DailyStatsManager()
    
    # Test update study time
    print("\n📚 Testing study time tracking...")
    stats.update_study_time(1800)  # 30 minutes
    stats.update_study_time(900)   # 15 minutes
    print(f"Current study time: {stats.get_today_summary()['study_time']}")
    
    # Test update break time
    print("\n☕ Testing break time tracking...")
    stats.update_break_time(300)   # 5 minutes
    stats.update_break_time(600)   # 10 minutes
    print(f"Current break time: {stats.get_today_summary()['break_time']}")
    
    # Test sessions and tasks
    print("\n🎯 Testing sessions and tasks...")
    stats.increment_sessions_completed()
    stats.increment_sessions_completed()
    stats.increment_tasks_completed()
    stats.increment_tasks_completed()
    stats.increment_tasks_completed()
    
    # Show today's summary
    print("\n📊 Today's Summary:")
    summary = stats.get_today_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    # Show weekly summary
    print("\n📈 Weekly Summary:")
    weekly = stats.get_weekly_total()
    for key, value in weekly.items():
        print(f"  {key}: {value}")
    
    # Show recent days
    print("\n📅 Recent 3 days:")
    recent = stats.get_recent_days(3)
    for day in recent:
        print(f"  {day['date']}: Study {day['formatted_study_time']}, Break {day['formatted_break_time']}")
    
    print("\n✅ All tests passed!")

if __name__ == "__main__":
    test_daily_stats()
