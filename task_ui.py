"""
Task UI Components - Giao diện quản lý tasks
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class TaskUI:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.tasks_frame = None
        self.task_listbox = None
        self.completed_listbox = None
        self.task_entry = None
        self.summary_label = None
        
        # Callbacks
        self.on_add_task = None
        self.on_complete_task = None
        self.on_delete_task = None
        self.on_edit_task = None
        
        self._create_task_widgets()

    def _create_task_widgets(self):
        """Tạo các widget cho task management"""
        # Main task frame
        self.tasks_frame = tk.Frame(self.parent_frame, bg='black')
        self.tasks_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Task summary
        summary_frame = tk.Frame(self.tasks_frame, bg='black')
        summary_frame.pack(fill=tk.X, pady=5)
        
        self.summary_label = tk.Label(
            summary_frame,
            text="Tasks: 0 total, 0 completed",
            font=("Courier New", 12, "bold"),
            fg="lightgreen",
            bg="black"
        )
        self.summary_label.pack()

        # Add task frame
        add_frame = tk.Frame(self.tasks_frame, bg='black')
        add_frame.pack(fill=tk.X, pady=5)

        tk.Label(add_frame, text="New Task:", fg="white", bg="black").pack(side=tk.LEFT)
        
        self.task_entry = tk.Entry(add_frame, width=30, font=("Arial", 10))
        self.task_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.task_entry.bind("<Return>", self._on_add_task_enter)

        self.add_btn = tk.Button(
            add_frame,
            text="Add Task",
            command=self._on_add_task_clicked,
            bg="green",
            fg="white",
            width=10
        )
        self.add_btn.pack(side=tk.RIGHT, padx=5)

        # Tasks display frame
        display_frame = tk.Frame(self.tasks_frame, bg='black')
        display_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Active tasks
        active_frame = tk.Frame(display_frame, bg='black')
        active_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        tk.Label(active_frame, text="📋 Active Tasks", fg="yellow", bg="black", 
                font=("Courier New", 11, "bold")).pack()

        # Active tasks listbox with scrollbar
        active_list_frame = tk.Frame(active_frame, bg='black')
        active_list_frame.pack(fill=tk.BOTH, expand=True)

        self.task_listbox = tk.Listbox(
            active_list_frame,
            height=6,
            font=("Arial", 9),
            bg="gray20",
            fg="white",
            selectbackground="blue"
        )
        
        active_scrollbar = tk.Scrollbar(active_list_frame)
        active_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.task_listbox.config(yscrollcommand=active_scrollbar.set)
        active_scrollbar.config(command=self.task_listbox.yview)

        # Active tasks buttons
        active_btn_frame = tk.Frame(active_frame, bg='black')
        active_btn_frame.pack(fill=tk.X, pady=2)

        self.complete_btn = tk.Button(
            active_btn_frame,
            text="✓ Complete",
            command=self._on_complete_task_clicked,
            bg="darkgreen",
            fg="white",
            width=8
        )
        self.complete_btn.pack(side=tk.LEFT, padx=2)

        self.edit_btn = tk.Button(
            active_btn_frame,
            text="✏️ Edit",
            command=self._on_edit_task_clicked,
            bg="orange",
            fg="white",
            width=8
        )
        self.edit_btn.pack(side=tk.LEFT, padx=2)

        self.delete_btn = tk.Button(
            active_btn_frame,
            text="🗑️ Delete",
            command=self._on_delete_task_clicked,
            bg="darkred",
            fg="white",
            width=8
        )
        self.delete_btn.pack(side=tk.LEFT, padx=2)

        # Completed tasks
        completed_frame = tk.Frame(display_frame, bg='black')
        completed_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        tk.Label(completed_frame, text="✅ Completed Tasks", fg="lightgreen", bg="black",
                font=("Courier New", 11, "bold")).pack()

        # Completed tasks listbox with scrollbar
        completed_list_frame = tk.Frame(completed_frame, bg='black')
        completed_list_frame.pack(fill=tk.BOTH, expand=True)

        self.completed_listbox = tk.Listbox(
            completed_list_frame,
            height=6,
            font=("Arial", 9),
            bg="gray15",
            fg="lightgray",
            selectbackground="darkgreen"
        )
        
        completed_scrollbar = tk.Scrollbar(completed_list_frame)
        completed_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.completed_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.completed_listbox.config(yscrollcommand=completed_scrollbar.set)
        completed_scrollbar.config(command=self.completed_listbox.yview)

        # Completed tasks buttons
        completed_btn_frame = tk.Frame(completed_frame, bg='black')
        completed_btn_frame.pack(fill=tk.X, pady=2)

        self.clear_completed_btn = tk.Button(
            completed_btn_frame,
            text="🧹 Clear All",
            command=self._on_clear_completed_clicked,
            bg="purple",
            fg="white",
            width=12
        )
        self.clear_completed_btn.pack()

    def _on_add_task_enter(self, event):
        """Xử lý Enter key trong task entry"""
        self._on_add_task_clicked()

    def _on_add_task_clicked(self):
        """Xử lý sự kiện thêm task"""
        task_text = self.task_entry.get().strip()
        if task_text and self.on_add_task:
            self.on_add_task(task_text)
            self.task_entry.delete(0, tk.END)

    def _on_complete_task_clicked(self):
        """Xử lý sự kiện hoàn thành task"""
        selection = self.task_listbox.curselection()
        if selection and self.on_complete_task:
            index = selection[0]
            self.on_complete_task(index)

    def _on_edit_task_clicked(self):
        """Xử lý sự kiện chỉnh sửa task"""
        selection = self.task_listbox.curselection()
        if selection and self.on_edit_task:
            index = selection[0]
            current_text = self.task_listbox.get(index)
            # Remove priority prefix if exists
            if current_text.startswith(('🔴 ', '🟡 ', '🟢 ')):
                current_text = current_text[2:]
            
            new_text = simpledialog.askstring("Edit Task", "Edit task:", initialvalue=current_text)
            if new_text:
                self.on_edit_task(index, new_text.strip())

    def _on_delete_task_clicked(self):
        """Xử lý sự kiện xóa task"""
        selection = self.task_listbox.curselection()
        if selection and self.on_delete_task:
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
                index = selection[0]
                self.on_delete_task(index)

    def _on_clear_completed_clicked(self):
        """Xử lý sự kiện xóa tất cả completed tasks"""
        if self.completed_listbox.size() > 0:
            if messagebox.askyesno("Clear Completed", "Clear all completed tasks?"):
                if hasattr(self, 'on_clear_completed') and self.on_clear_completed:
                    self.on_clear_completed()

    def update_task_list(self, tasks):
        """Cập nhật danh sách tasks"""
        self.task_listbox.delete(0, tk.END)
        for task in tasks:
            # Add priority indicator
            priority_icon = {'high': '🔴', 'normal': '🟡', 'low': '🟢'}.get(task.get('priority', 'normal'), '🟡')
            display_text = f"{priority_icon} {task['text']}"
            self.task_listbox.insert(tk.END, display_text)

    def update_completed_list(self, completed_tasks):
        """Cập nhật danh sách completed tasks"""
        self.completed_listbox.delete(0, tk.END)
        for task in completed_tasks:
            self.completed_listbox.insert(tk.END, f"✅ {task['text']}")

    def update_summary(self, summary):
        """Cập nhật task summary"""
        text = f"Tasks: {summary['total']} total, {summary['completed']} completed ({summary['completion_rate']:.1f}%)"
        self.summary_label.config(text=text)

    def show_task_complete_notification(self, task):
        """Hiển thị thông báo hoàn thành task"""
        messagebox.showinfo("Task Completed", f"✅ Completed: {task['text']}")

    def get_frame(self):
        """Trả về frame chính của task UI"""
        return self.tasks_frame
