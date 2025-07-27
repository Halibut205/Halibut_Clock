"""
Daily Statistics Manager - Quản lý thống kê học tập hàng ngày
"""
import json
import os
from datetime import datetime, date, timedelta
from typing import Dict, Any, Optional, List

class DailyStatsManager:
    """
    Manages daily study statistics and data persistence.
    
    Handles tracking of study time, break time, sessions completed,
    and tasks completed with flexible data querying capabilities.
    """
    
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
    
    def get_date_stats(self, date_str: str) -> Dict[str, Any]:
        """Lấy thống kê của ngày cụ thể (format: YYYY-MM-DD)"""
        if date_str in self.stats_data:
            return self.stats_data[date_str]
        else:
            # Trả về empty stats nếu không có dữ liệu
            return {
                "date": date_str,
                "study_time": 0,
                "break_time": 0,
                "sessions_completed": 0,
                "tasks_completed": 0,
                "start_time": None,
                "last_update": None
            }
    
    def get_date_summary(self, date_str: str) -> Dict[str, str]:
        """Lấy tóm tắt thống kê của ngày cụ thể với format đẹp"""
        date_stats = self.get_date_stats(date_str)
        return {
            "date": date_stats["date"],
            "study_time": self.format_time(date_stats["study_time"]),
            "break_time": self.format_time(date_stats["break_time"]),
            "sessions_completed": str(date_stats["sessions_completed"]),
            "tasks_completed": str(date_stats["tasks_completed"]),
            "total_time": self.format_time(date_stats["study_time"] + date_stats["break_time"])
        }
    
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
    
    def get_recent_days(self, days: int = 7) -> List[Dict[str, Any]]:
        """Lấy thống kê của N ngày gần đây"""
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
                recent_stats.append(self._create_empty_day_stats(date_key))
        
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
        from calendar import monthrange
        
        # Nếu không chỉ định, lấy tháng hiện tại
        if year is None or month is None:
            now = datetime.now()
            year = now.year
            month = now.month
        
        # Lấy số ngày trong tháng
        days_in_month = monthrange(year, month)[1]
        
        monthly_stats = []
        totals = {"study": 0, "break": 0, "sessions": 0, "tasks": 0}
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
                totals["study"] += day_stats["study_time"]
                totals["break"] += day_stats["break_time"]
                totals["sessions"] += day_stats["sessions_completed"]
                totals["tasks"] += day_stats["tasks_completed"]
                
                if day_stats["study_time"] > 0:
                    active_days += 1
            else:
                # Ngày không có dữ liệu
                monthly_stats.append(self._create_empty_day_stats(date_key))
        
        return {
            "year": year,
            "month": month,
            "month_name": datetime(year, month, 1).strftime("%B %Y"),
            "days_in_month": days_in_month,
            "daily_stats": monthly_stats,
            "total_study_time": self.format_time(totals["study"]),
            "total_break_time": self.format_time(totals["break"]),
            "total_sessions": totals["sessions"],
            "total_tasks": totals["tasks"],
            "active_days": active_days,
            "average_daily_study": self.format_time(totals["study"] // days_in_month),
            "productivity_rate": f"{(active_days / days_in_month * 100):.1f}%"
        }
    
    def get_month_comparison(self, months_back: int = 3) -> List[Dict[str, Any]]:
        """So sánh thống kê của N tháng gần đây"""
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
    
    def get_best_days_in_month(self, year: int = None, month: int = None, top_n: int = 5) -> List[Dict[str, Any]]:
        """Lấy những ngày học tập tốt nhất trong tháng"""
        monthly_data = self.get_monthly_data(year, month)
        
        # Lọc những ngày có hoạt động học tập
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

    def _create_empty_day_stats(self, date_key: str) -> Dict[str, Any]:
        """Tạo entry trống cho ngày không có dữ liệu"""
        return {
            "date": date_key,
            "study_time": 0,
            "break_time": 0,
            "sessions_completed": 0,
            "tasks_completed": 0,
            "formatted_study_time": "00:00:00",
            "formatted_break_time": "00:00:00"
        }

    def get_data_range(self, start_date=None, end_date=None, days=None) -> List[Dict[str, Any]]:
        """
        Lấy dữ liệu trong khoảng thời gian linh hoạt
        
        Args:
            start_date: Ngày bắt đầu (datetime.date hoặc string YYYY-MM-DD)
            end_date: Ngày kết thúc (datetime.date hoặc string YYYY-MM-DD)
            days: Số ngày gần đây (ưu tiên nếu start_date = None)
        
        Returns:
            List dữ liệu đã được sắp xếp theo thời gian
        """
        # Xác định end_date
        if end_date is None:
            end_date = date.today()
        elif isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        
        # Xác định start_date
        if start_date is None:
            if days is None:
                days = 30  # Mặc định 30 ngày
            start_date = end_date - timedelta(days=days-1)
        elif isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        
        # Tạo danh sách ngày trong khoảng thời gian
        current_date = start_date
        range_stats = []
        
        while current_date <= end_date:
            date_key = current_date.isoformat()
            
            if date_key in self.stats_data:
                stats = self.stats_data[date_key].copy()
                stats["formatted_study_time"] = self.format_time(stats["study_time"])
                stats["formatted_break_time"] = self.format_time(stats["break_time"])
                range_stats.append(stats)
            else:
                # Tạo entry trống cho ngày không có dữ liệu
                range_stats.append(self._create_empty_day_stats(date_key))
            
            current_date += timedelta(days=1)
        
        return range_stats

    def get_yearly_data(self, year=None) -> Dict[str, Any]:
        """
        Lấy toàn bộ dữ liệu của một năm
        
        Args:
            year: Năm cần lấy dữ liệu (nếu None thì lấy năm hiện tại)
        
        Returns:
            Dictionary chứa thống kê tổng hợp của năm
        """
        if year is None:
            year = datetime.now().year
        
        yearly_stats = []
        totals = {"study": 0, "break": 0, "sessions": 0, "tasks": 0}
        active_days = 0
        
        # Duyệt qua tất cả 12 tháng
        for month in range(1, 13):
            monthly_data = self.get_monthly_data(year, month)
            
            # Chuyển đổi total_study_time từ string sang seconds để tính tổng
            month_study_seconds = self.time_to_seconds(monthly_data["total_study_time"])
            month_break_seconds = self.time_to_seconds(monthly_data["total_break_time"])
            
            # Thêm tháng vào yearly_stats
            yearly_stats.append({
                "month": month,
                "month_name": monthly_data["month_name"],
                "total_study_time": monthly_data["total_study_time"],
                "total_break_time": monthly_data["total_break_time"],
                "total_sessions": monthly_data["total_sessions"],
                "total_tasks": monthly_data["total_tasks"],
                "active_days": monthly_data["active_days"],
                "days_in_month": monthly_data["days_in_month"],
                "productivity_rate": monthly_data["productivity_rate"],
                "daily_stats": monthly_data["daily_stats"]
            })
            
            # Tích lũy thống kê tổng
            totals["study"] += month_study_seconds
            totals["break"] += month_break_seconds
            totals["sessions"] += monthly_data["total_sessions"]
            totals["tasks"] += monthly_data["total_tasks"]
            active_days += monthly_data["active_days"]
        
        return {
            "year": year,
            "monthly_stats": yearly_stats,
            "total_study_time": self.format_time(totals["study"]),
            "total_break_time": self.format_time(totals["break"]),
            "total_sessions": totals["sessions"],
            "total_tasks": totals["tasks"],
            "active_days": active_days,
            "average_daily_study": self.format_time(totals["study"] // 365) if totals["study"] > 0 else "00:00:00",
            "study_hours_per_month": totals["study"] / 3600 / 12 if totals["study"] > 0 else 0,
            "productivity_rate": f"{(active_days / 365 * 100):.1f}%"
        }

    def time_to_seconds(self, time_str: str) -> int:
        """
        Chuyển đổi chuỗi thời gian HH:MM:SS thành giây
        
        Args:
            time_str: Chuỗi thời gian dạng "HH:MM:SS"
        
        Returns:
            Số giây (int)
        """
        try:
            parts = time_str.split(":")
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        except (ValueError, IndexError):
            return 0

    def get_available_years(self) -> List[int]:
        """Lấy danh sách các năm có dữ liệu"""
        if not self.stats_data:
            return []
        
        years = set()
        for date_key in self.stats_data.keys():
            try:
                year = int(date_key.split('-')[0])
                years.add(year)
            except (ValueError, IndexError):
                continue
        
        return sorted(list(years), reverse=True)

    def get_available_months_in_year(self, year: int) -> List[int]:
        """Lấy danh sách các tháng có dữ liệu trong năm"""
        if not self.stats_data:
            return []
        
        months = set()
        year_str = str(year)
        
        for date_key in self.stats_data.keys():
            if date_key.startswith(year_str):
                try:
                    month = int(date_key.split('-')[1])
                    months.add(month)
                except (ValueError, IndexError):
                    continue
        
        return sorted(list(months))

    def get_data_summary(self) -> Dict[str, Any]:
        """
        Lấy tóm tắt tổng thể về dữ liệu
        
        Returns:
            Dictionary chứa thống kê tổng quan
        """
        if not self.stats_data:
            return {
                "total_days_recorded": 0,
                "earliest_date": None,
                "latest_date": None,
                "total_study_hours": 0,
                "total_sessions": 0,
                "total_tasks": 0,
                "average_study_per_day": 0,
                "available_years": [],
                "total_years": 0
            }
        
        dates = sorted(self.stats_data.keys())
        total_study = sum(day.get("study_time", 0) for day in self.stats_data.values())
        total_sessions = sum(day.get("sessions_completed", 0) for day in self.stats_data.values())
        total_tasks = sum(day.get("tasks_completed", 0) for day in self.stats_data.values())
        available_years = self.get_available_years()
        
        return {
            "total_days_recorded": len(self.stats_data),
            "earliest_date": dates[0],
            "latest_date": dates[-1],
            "total_study_hours": total_study / 3600,
            "total_sessions": total_sessions,
            "total_tasks": total_tasks,
            "average_study_per_day": total_study / len(self.stats_data) / 3600 if len(self.stats_data) > 0 else 0,
            "available_years": available_years,
            "total_years": len(available_years)
        }
    
    def get_monthly_average_study_time(self, year: int = None, month: int = None) -> float:
        """
        Tính trung bình thời gian học tập theo ngày trong tháng
        
        Args:
            year: Năm (mặc định là năm hiện tại)
            month: Tháng (mặc định là tháng hiện tại)
            
        Returns:
            float: Trung bình giờ học/ngày trong tháng (giờ)
        """
        if year is None or month is None:
            current_date = date.today()
            year = year or current_date.year
            month = month or current_date.month
        
        # Lấy dữ liệu tháng
        monthly_data = self.get_monthly_data(year, month)
        
        if not monthly_data:
            return 4.0  # Default 4h nếu không có dữ liệu
        
        # Tính tổng thời gian học và số ngày có dữ liệu
        total_study_seconds = 0
        days_with_data = 0
        
        for day_data in monthly_data.values():
            if isinstance(day_data, dict) and 'study_time' in day_data:
                study_time = day_data['study_time']
                if study_time > 0:  # Chỉ tính những ngày có học
                    total_study_seconds += study_time
                    days_with_data += 1
        
        if days_with_data == 0:
            return 4.0  # Default 4h nếu không có ngày nào có dữ liệu
        
        # Trả về trung bình theo giờ
        average_seconds_per_day = total_study_seconds / days_with_data
        return average_seconds_per_day / 3600  # Convert to hours
    
    def get_monthly_average_sessions(self, year: int = None, month: int = None) -> float:
        """
        Tính trung bình số sessions theo ngày trong tháng
        
        Args:
            year: Năm (mặc định là năm hiện tại)
            month: Tháng (mặc định là tháng hiện tại)
            
        Returns:
            float: Trung bình sessions/ngày trong tháng
        """
        if year is None or month is None:
            current_date = date.today()
            year = year or current_date.year
            month = month or current_date.month
        
        # Lấy dữ liệu tháng
        monthly_data = self.get_monthly_data(year, month)
        
        if not monthly_data:
            return 4.0  # Default 4 sessions nếu không có dữ liệu
        
        # Tính tổng sessions và số ngày có dữ liệu
        total_sessions = 0
        days_with_data = 0
        
        for day_data in monthly_data.values():
            if isinstance(day_data, dict) and 'sessions_completed' in day_data:
                sessions = day_data['sessions_completed']
                if sessions > 0:  # Chỉ tính những ngày có sessions
                    total_sessions += sessions
                    days_with_data += 1
        
        if days_with_data == 0:
            return 4.0  # Default 4 sessions nếu không có ngày nào có dữ liệu
        
        # Trả về trung bình sessions
        return total_sessions / days_with_data

    def get_dynamic_session_goal(self, target_date: date = None) -> int:
        """
        Tính daily session goal động dựa trên trung bình sessions của tháng + 2
        
        Args:
            target_date: Ngày cần tính goal (mặc định là hôm nay)
            
        Returns:
            int: Daily session goal (sessions trung bình + 2)
        """
        if target_date is None:
            target_date = date.today()
        
        # Lấy trung bình sessions tháng hiện tại
        monthly_avg_sessions = self.get_monthly_average_sessions(target_date.year, target_date.month)
        
        # Trung bình + 2, tối thiểu 3, tối đa 12
        goal = max(3, min(12, int(round(monthly_avg_sessions + 2))))
        return goal

    def get_dynamic_daily_goal(self, target_date: date = None) -> float:
        """
        Tính daily goal động dựa trên trung bình tháng
        
        Args:
            target_date: Ngày cần tính goal (mặc định là hôm nay)
            
        Returns:
            float: Daily goal tính theo giờ
        """
        if target_date is None:
            target_date = date.today()
        
        # Lấy trung bình tháng hiện tại
        monthly_avg = self.get_monthly_average_study_time(target_date.year, target_date.month)
        
        # Đảm bảo goal tối thiểu là 2h, tối đa là 8h
        return max(2.0, min(8.0, monthly_avg))
