"""
Daily Statistics Manager - Quản lý thống kê học tập hàng ngày
"""
import json
import os
from datetime import datetime, date
from typing import Dict, Any, Optional

class DailyStatsManager:
    def __init__(self, data_folder="data"):
        self.data_folder = data_folder
        self.stats_file = os.path.join(data_folder, "daily_stats.json")
        self.ensure_data_folder()
        self.stats_data = self.load_stats()
        
    def ensure_data_folder(self):
        """Đảm bảo thư mục data tồn tại"""
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
    
    def load_stats(self) -> Dict[str, Any]:
        """Tải dữ liệu thống kê từ file"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}
    
    def save_stats(self):
        """Lưu dữ liệu thống kê vào file"""
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving daily stats: {e}")
    
    def get_today_key(self) -> str:
        """Lấy key cho ngày hôm nay (YYYY-MM-DD)"""
        return date.today().isoformat()
    
    def get_today_stats(self) -> Dict[str, Any]:
        """Lấy thống kê của ngày hôm nay"""
        today_key = self.get_today_key()
        if today_key not in self.stats_data:
            self.stats_data[today_key] = {
                "date": today_key,
                "study_time": 0,  # Thời gian học (giây)
                "break_time": 0,  # Thời gian nghỉ (giây)
                "sessions_completed": 0,
                "tasks_completed": 0,
                "start_time": None,  # Thời gian bắt đầu học đầu tiên
                "last_update": None  # Lần cập nhật cuối
            }
        return self.stats_data[today_key]
    
    def update_study_time(self, additional_seconds: int):
        """Cập nhật thời gian học"""
        today_stats = self.get_today_stats()
        today_stats["study_time"] += additional_seconds
        today_stats["last_update"] = datetime.now().isoformat()
        
        # Đặt thời gian bắt đầu nếu chưa có
        if today_stats["start_time"] is None:
            today_stats["start_time"] = datetime.now().isoformat()
        
        self.save_stats()
    
    def update_break_time(self, additional_seconds: int):
        """Cập nhật thời gian nghỉ"""
        today_stats = self.get_today_stats()
        today_stats["break_time"] += additional_seconds
        today_stats["last_update"] = datetime.now().isoformat()
        self.save_stats()
    
    def increment_sessions_completed(self):
        """Tăng số session đã hoàn thành"""
        today_stats = self.get_today_stats()
        today_stats["sessions_completed"] += 1
        today_stats["last_update"] = datetime.now().isoformat()
        self.save_stats()
    
    def increment_tasks_completed(self):
        """Tăng số task đã hoàn thành"""
        today_stats = self.get_today_stats()
        today_stats["tasks_completed"] += 1
        today_stats["last_update"] = datetime.now().isoformat()
        self.save_stats()
    
    def format_time(self, seconds: int) -> str:
        """Format thời gian thành HH:MM:SS"""
        hrs = seconds // 3600
        mins = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hrs:02}:{mins:02}:{secs:02}"
    
    def get_today_summary(self) -> Dict[str, str]:
        """Lấy tóm tắt thống kê ngày hôm nay"""
        today_stats = self.get_today_stats()
        return {
            "date": today_stats["date"],
            "study_time": self.format_time(today_stats["study_time"]),
            "break_time": self.format_time(today_stats["break_time"]),
            "sessions_completed": str(today_stats["sessions_completed"]),
            "tasks_completed": str(today_stats["tasks_completed"]),
            "total_time": self.format_time(today_stats["study_time"] + today_stats["break_time"])
        }
    
    def get_recent_days(self, days: int = 7) -> list:
        """Lấy thống kê của N ngày gần đây"""
        from datetime import timedelta
        recent_stats = []
        
        for i in range(days):
            target_date = date.today() - timedelta(days=i)
            date_key = target_date.isoformat()
            
            if date_key in self.stats_data:
                stats = self.stats_data[date_key].copy()
                stats["formatted_study_time"] = self.format_time(stats["study_time"])
                stats["formatted_break_time"] = self.format_time(stats["break_time"])
                recent_stats.append(stats)
            else:
                # Tạo entry trống cho ngày không có dữ liệu
                recent_stats.append({
                    "date": date_key,
                    "study_time": 0,
                    "break_time": 0,
                    "sessions_completed": 0,
                    "tasks_completed": 0,
                    "formatted_study_time": "00:00:00",
                    "formatted_break_time": "00:00:00"
                })
        
        return recent_stats
    
    def get_weekly_total(self) -> Dict[str, Any]:
        """Lấy tổng thống kê tuần này"""
        recent_days = self.get_recent_days(7)
        total_study = sum(day["study_time"] for day in recent_days)
        total_break = sum(day["break_time"] for day in recent_days)
        total_sessions = sum(day["sessions_completed"] for day in recent_days)
        total_tasks = sum(day["tasks_completed"] for day in recent_days)
        
        return {
            "total_study_time": self.format_time(total_study),
            "total_break_time": self.format_time(total_break),
            "total_sessions": total_sessions,
            "total_tasks": total_tasks,
            "average_daily_study": self.format_time(total_study // 7),
            "days_active": len([day for day in recent_days if day["study_time"] > 0])
        }
    
    def get_monthly_data(self, year: int = None, month: int = None) -> Dict[str, Any]:
        """Lấy thống kê theo tháng"""
        from datetime import datetime
        from calendar import monthrange
        
        # Nếu không chỉ định, lấy tháng hiện tại
        if year is None or month is None:
            now = datetime.now()
            year = now.year
            month = now.month
        
        # Lấy số ngày trong tháng
        days_in_month = monthrange(year, month)[1]
        
        monthly_stats = []
        total_study = 0
        total_break = 0
        total_sessions = 0
        total_tasks = 0
        active_days = 0
        
        # Duyệt qua tất cả ngày trong tháng
        for day in range(1, days_in_month + 1):
            date_key = f"{year:04d}-{month:02d}-{day:02d}"
            
            if date_key in self.stats_data:
                day_stats = self.stats_data[date_key].copy()
                day_stats["formatted_study_time"] = self.format_time(day_stats["study_time"])
                day_stats["formatted_break_time"] = self.format_time(day_stats["break_time"])
                monthly_stats.append(day_stats)
                
                # Tính tổng
                total_study += day_stats["study_time"]
                total_break += day_stats["break_time"]
                total_sessions += day_stats["sessions_completed"]
                total_tasks += day_stats["tasks_completed"]
                
                if day_stats["study_time"] > 0:
                    active_days += 1
            else:
                # Ngày không có dữ liệu
                monthly_stats.append({
                    "date": date_key,
                    "study_time": 0,
                    "break_time": 0,
                    "sessions_completed": 0,
                    "tasks_completed": 0,
                    "formatted_study_time": "00:00:00",
                    "formatted_break_time": "00:00:00"
                })
        
        return {
            "year": year,
            "month": month,
            "month_name": datetime(year, month, 1).strftime("%B %Y"),
            "days_in_month": days_in_month,
            "daily_stats": monthly_stats,
            "total_study_time": self.format_time(total_study),
            "total_break_time": self.format_time(total_break),
            "total_sessions": total_sessions,
            "total_tasks": total_tasks,
            "active_days": active_days,
            "average_daily_study": self.format_time(total_study // days_in_month),
            "productivity_rate": f"{(active_days / days_in_month * 100):.1f}%"
        }
    
    def get_month_comparison(self, months_back: int = 3) -> list:
        """So sánh thống kê của N tháng gần đây"""
        from datetime import datetime, timedelta
        import calendar
        
        comparisons = []
        current_date = datetime.now()
        
        for i in range(months_back):
            # Tính tháng trước
            if current_date.month - i > 0:
                target_month = current_date.month - i
                target_year = current_date.year
            else:
                target_month = 12 + (current_date.month - i)
                target_year = current_date.year - 1
            
            monthly_data = self.get_monthly_data(target_year, target_month)
            comparisons.append({
                "month_name": monthly_data["month_name"],
                "study_time": monthly_data["total_study_time"],
                "active_days": monthly_data["active_days"],
                "sessions": monthly_data["total_sessions"],
                "tasks": monthly_data["total_tasks"],
                "productivity_rate": monthly_data["productivity_rate"]
            })
        
        return comparisons
    
    def get_best_days_in_month(self, year: int = None, month: int = None, top_n: int = 5) -> list:
        """Lấy những ngày học tập tốt nhất trong tháng"""
        monthly_data = self.get_monthly_data(year, month)
        
        # Sắp xếp theo thời gian học (study_time)
        daily_stats = monthly_data["daily_stats"]
        active_days = [day for day in daily_stats if day["study_time"] > 0]
        
        # Sắp xếp theo thời gian học giảm dần
        best_days = sorted(active_days, key=lambda x: x["study_time"], reverse=True)[:top_n]
        
        # Format ngày hiển thị đẹp hơn
        for day in best_days:
            date_obj = datetime.strptime(day["date"], "%Y-%m-%d")
            day["display_date"] = date_obj.strftime("%B %d (%A)")
        
        return best_days
    
    def reset_today(self):
        """Reset thống kê ngày hôm nay"""
        today_key = self.get_today_key()
        if today_key in self.stats_data:
            del self.stats_data[today_key]
            self.save_stats()
