"""
Task Manager Module - Quản lý các task và tiến độ hoàn thành
"""

import json
import os
from datetime import datetime

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.completed_tasks = []
        self.data_file = os.path.join(os.path.dirname(__file__), "..", "..", "data", "tasks_data.json")
        self.load_tasks()
        
        # Callbacks
        self.on_task_added = None
        self.on_task_completed = None
        self.on_task_deleted = None
        self.on_tasks_updated = None

    def add_task(self, task_text, session_target=None):
        """Thêm task mới"""
        task = {
            'id': len(self.tasks) + len(self.completed_tasks) + 1,
            'text': task_text,
            'created_at': datetime.now().isoformat(),
            'session_target': session_target,  # Session nào muốn hoàn thành task này
            'priority': 'normal'  # normal, high, low
        }
        
        self.tasks.append(task)
        self.save_tasks()
        
        if self.on_task_added:
            self.on_task_added(task)
        if self.on_tasks_updated:
            self.on_tasks_updated()
        
        return task

    def complete_task(self, task_id):
        """Đánh dấu task hoàn thành"""
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                task['completed_at'] = datetime.now().isoformat()
                completed_task = self.tasks.pop(i)
                self.completed_tasks.append(completed_task)
                self.save_tasks()
                
                if self.on_task_completed:
                    self.on_task_completed(completed_task)
                if self.on_tasks_updated:
                    self.on_tasks_updated()
                
                return completed_task
        return None

    def delete_task(self, task_id, from_completed=False):
        """Xóa task"""
        task_list = self.completed_tasks if from_completed else self.tasks
        
        for i, task in enumerate(task_list):
            if task['id'] == task_id:
                deleted_task = task_list.pop(i)
                self.save_tasks()
                
                if self.on_task_deleted:
                    self.on_task_deleted(deleted_task)
                if self.on_tasks_updated:
                    self.on_tasks_updated()
                
                return deleted_task
        return None

    def get_tasks_for_session(self, session_number):
        """Lấy tasks cho session cụ thể"""
        return [task for task in self.tasks if task.get('session_target') == session_number]

    def get_all_active_tasks(self):
        """Lấy tất cả tasks chưa hoàn thành"""
        return self.tasks.copy()

    def get_completed_tasks(self):
        """Lấy tất cả tasks đã hoàn thành"""
        return self.completed_tasks.copy()

    def get_tasks_summary(self):
        """Lấy tóm tắt về tasks"""
        total_tasks = len(self.tasks) + len(self.completed_tasks)
        completed_count = len(self.completed_tasks)
        remaining_count = len(self.tasks)
        
        completion_rate = (completed_count / total_tasks * 100) if total_tasks > 0 else 0
        
        return {
            'total': total_tasks,
            'completed': completed_count,
            'remaining': remaining_count,
            'completion_rate': completion_rate
        }

    def set_task_priority(self, task_id, priority):
        """Thiết lập priority cho task"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['priority'] = priority
                self.save_tasks()
                if self.on_tasks_updated:
                    self.on_tasks_updated()
                return True
        return False

    def edit_task(self, task_id, new_text):
        """Chỉnh sửa nội dung task"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['text'] = new_text
                task['updated_at'] = datetime.now().isoformat()
                self.save_tasks()
                if self.on_tasks_updated:
                    self.on_tasks_updated()
                return True
        return False

    def clear_completed_tasks(self):
        """Xóa tất cả tasks đã hoàn thành"""
        cleared_count = len(self.completed_tasks)
        self.completed_tasks.clear()
        self.save_tasks()
        
        if self.on_tasks_updated:
            self.on_tasks_updated()
        
        return cleared_count

    def save_tasks(self):
        """Lưu tasks vào file"""
        try:
            data = {
                'tasks': self.tasks,
                'completed_tasks': self.completed_tasks,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ Could not save tasks: {e}")

    def load_tasks(self):
        """Load tasks từ file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = data.get('tasks', [])
                    self.completed_tasks = data.get('completed_tasks', [])
                    print(f"✅ Loaded {len(self.tasks)} active tasks and {len(self.completed_tasks)} completed tasks")
            else:
                print("📝 No existing tasks file found, starting fresh")
        except Exception as e:
            print(f"❌ Could not load tasks: {e}")
            self.tasks = []
            self.completed_tasks = []
