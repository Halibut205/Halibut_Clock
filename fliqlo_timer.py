import tkinter as tk
from tkinter import font as tkfont

class FliqloTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fliqlo Timer")
        self.root.configure(bg='black')
        self.root.geometry("600x300")
        self.running = False
        self.time_elapsed = 0  # tính bằng giây
        self.break_running = False
        self.break_time = 0  # thời gian nghỉ

        # Font lớn, đậm, dễ đọc kiểu Fliqlo
        self.clock_font = tkfont.Font(family="Courier New", size=72, weight="bold")

        self.label = tk.Label(root, text="00:00:00", font=self.clock_font, fg="white", bg="black")
        self.label.pack(pady=40)

        # Break timer label (màu xanh)
        self.break_label = tk.Label(root, text="", font=tkfont.Font(family="Courier New", size=36, weight="bold"), 
                                   fg="cyan", bg="black")
        self.break_label.pack(pady=10)

        # Button frame
        btn_frame = tk.Frame(root, bg='black')
        btn_frame.pack()

        self.start_btn = tk.Button(btn_frame, text="Start", width=10, command=self.start_timer)
        self.start_btn.grid(row=0, column=0, padx=5)

        self.stop_btn = tk.Button(btn_frame, text="Pause", width=10, command=self.toggle_timer)
        self.stop_btn.grid(row=0, column=1, padx=5)

        self.reset_btn = tk.Button(btn_frame, text="Reset", width=10, command=self.reset_timer)
        self.reset_btn.grid(row=0, column=2, padx=5)

    def format_time(self, seconds):
        hrs = seconds // 3600
        mins = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hrs:02}:{mins:02}:{secs:02}"

    def update_timer(self):
        if self.running:
            self.time_elapsed += 1
            self.label.config(text=self.format_time(self.time_elapsed))
            self.root.after(1000, self.update_timer)
    
    def update_break_timer(self):
        if self.break_running:
            self.break_time += 1
            self.break_label.config(text=f"Break: {self.format_time(self.break_time)}")
            self.root.after(1000, self.update_break_timer)

    def start_timer(self):
        if not self.running:
            self.running = True
            self.time_elapsed = 0
            self.stop_btn.config(text="Pause")  # Đặt lại text của nút
            self.break_running = False  # Dừng break timer nếu có
            self.break_label.config(text="")  # Xóa hiển thị break timer
            self.update_timer()

    def toggle_timer(self):
        if self.running:
            # Nếu đang chạy thì pause
            self.running = False
            self.stop_btn.config(text="Resume")
            # Bắt đầu đồng hồ nghỉ khi pause
            if not self.break_running:
                self.break_running = True
                self.break_time = 0
                self.update_break_timer()
        else:
            # Nếu đang pause thì resume
            self.running = True
            self.stop_btn.config(text="Pause")
            # Dừng đồng hồ nghỉ khi resume - freeze tại thời điểm hiện tại
            self.break_running = False
            self.update_timer()

    def stop_timer(self):
        self.running = False
        # Bắt đầu đồng hồ nghỉ khi dừng timer chính
        if not self.break_running:
            self.break_running = True
            self.break_time = 0
            self.update_break_timer()

    def reset_timer(self):
        self.running = False
        self.break_running = False  # Dừng đồng hồ nghỉ khi reset
        self.time_elapsed = 0
        self.break_time = 0  # Reset thời gian nghỉ
        self.label.config(text="00:00:00")
        self.break_label.config(text="")  # Xóa label nghỉ
        self.stop_btn.config(text="Pause")  # Đặt lại text của nút

if __name__ == "__main__":
    root = tk.Tk()
    app = FliqloTimerApp(root)
    root.mainloop()
