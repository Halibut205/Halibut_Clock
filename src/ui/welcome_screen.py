# -*- coding: utf-8 -*-
"""
Welcome Screen Module - Màn hình giới thiệu về Pomodoro và cách sử dụng
"""

import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from .app_settings import mark_welcome_shown

class WelcomeScreen:
    def __init__(self, root, on_start_callback):
        self.root = root
        self.on_start_callback = on_start_callback
        self.dont_show_again = tk.BooleanVar()
        self.play_sound = None  # Sound callback
        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        """Setup cửa sổ welcome"""
        self.root.title("Fliqlo Timer - Welcome")
        self.root.configure(bg='black')
        self.root.geometry("800x900")
        self.root.resizable(True, True)
        
        # Center window
        self.root.eval('tk::PlaceWindow . center')

    def create_widgets(self):
        """Tạo các widget cho welcome screen"""
        # Credit
        credit_font = tkfont.Font(family="Arial", size=10, slant="italic")
        credit_label = tk.Label(
            self.root,
            text="Created by Halibut",
            font=credit_font,
            fg="gray",
            bg="black"
        )
        credit_label.pack(pady=(10, 0))
        
        # Title
        try:
            title_font = tkfont.Font(family="Courier New", size=28, weight="bold")
        except:
            title_font = tkfont.Font(family="Arial", size=28, weight="bold")
            
        title_label = tk.Label(
            self.root,
            text="🕐 Fliqlo Study Timer",
            font=title_font,
            fg="white",
            bg="black"
        )
        title_label.pack(pady=(10, 5))

        # Subtitle bilingual
        subtitle_font = tkfont.Font(family="Arial", size=14)
        subtitle_label = tk.Label(
            self.root,
            text="Pomodoro Technique & Study Session Manager\nỨng dụng quản lý thời gian học tập theo phương pháp Pomodoro",
            font=subtitle_font,
            fg="cyan",
            bg="black",
            justify='center'
        )
        subtitle_label.pack(pady=5)

        # Create scrollable frame
        self.create_scrollable_content()

        # Bottom buttons (outside scroll area)
        self.create_bottom_buttons()

    def create_scrollable_content(self):
        """Tạo nội dung có thể scroll"""
        # Main canvas and scrollbar frame
        canvas_frame = tk.Frame(self.root, bg='black')
        canvas_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Canvas for scrolling
        self.canvas = tk.Canvas(canvas_frame, bg='black', highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient='vertical', command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='black')

        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mouse wheel to canvas
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Add content to scrollable frame
        content_frame = tk.Frame(self.scrollable_frame, bg='black')
        content_frame.pack(pady=20, padx=40, fill='both', expand=True)

        # Pomodoro explanation
        self.create_pomodoro_section(content_frame)
        
        # How to use section
        self.create_howto_section(content_frame)
        
        # Features section
        self.create_features_section(content_frame)

    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def create_pomodoro_section(self, parent):
        """Tạo section giải thích về Pomodoro"""
        # Section title
        section_font = tkfont.Font(family="Arial", size=16, weight="bold")
        pomodoro_title = tk.Label(
            parent,
            text="🍅 What is Pomodoro Technique? / Phương pháp Pomodoro là gì?",
            font=section_font,
            fg="yellow",
            bg="black"
        )
        pomodoro_title.pack(anchor='w', pady=(0, 10))

        # Pomodoro explanation bilingual
        text_font = tkfont.Font(family="Arial", size=12)
        pomodoro_text = """
🇺🇸 English:
• Work in focused 25-minute intervals called "Pomodoros"
• Take a 5-minute break after each Pomodoro
• After 4 Pomodoros, take a longer 15-30 minute break
• Helps maintain focus and prevent burnout
• Increases productivity and time awareness

🇻🇳 Tiếng Việt:
• Làm việc tập trung trong khoảng thời gian 25 phút gọi là "Pomodoro"
• Nghỉ 5 phút sau mỗi Pomodoro
• Sau 4 Pomodoro, nghỉ dài hơn 15-30 phút
• Giúp duy trì sự tập trung và tránh kiệt sức
• Tăng năng suất và ý thức về thời gian
        """.strip()
        
        pomodoro_label = tk.Label(
            parent,
            text=pomodoro_text,
            font=text_font,
            fg="white",
            bg="black",
            justify='left'
        )
        pomodoro_label.pack(anchor='w', pady=(0, 20))

    def create_howto_section(self, parent):
        """Tạo section hướng dẫn sử dụng"""
        section_font = tkfont.Font(family="Arial", size=16, weight="bold")
        howto_title = tk.Label(
            parent,
            text="🎮 How to Use This App / Cách sử dụng ứng dụng",
            font=section_font,
            fg="orange",
            bg="black"
        )
        howto_title.pack(anchor='w', pady=(0, 10))

        text_font = tkfont.Font(family="Arial", size=12)
        howto_text = """
🇺🇸 English:
1. Choose session duration: 15min, 25min (Pomodoro), 45min, 1-2 hours
2. Set your daily session target (default: 8 sessions)
3. Add tasks you want to work on during sessions
4. Click START to begin your focused work session
5. Take breaks when the timer suggests (auto-break feature)
6. Complete tasks and track your progress

🇻🇳 Tiếng Việt:
1. Chọn thời lượng session: 15 phút, 25 phút (Pomodoro), 45 phút, 1-2 giờ
2. Đặt mục tiêu session hàng ngày (mặc định: 8 session)
3. Thêm các task muốn làm trong session
4. Nhấn START để bắt đầu session tập trung
5. Nghỉ ngơi khi timer gợi ý (tính năng tự động nghỉ)
6. Hoàn thành task và theo dõi tiến độ
        """.strip()
        
        howto_label = tk.Label(
            parent,
            text=howto_text,
            font=text_font,
            fg="white",
            bg="black",
            justify='left'
        )
        howto_label.pack(anchor='w', pady=(0, 20))

    def create_features_section(self, parent):
        """Tạo section features"""
        section_font = tkfont.Font(family="Arial", size=16, weight="bold")
        features_title = tk.Label(
            parent,
            text="✨ Key Features / Tính năng chính",
            font=section_font,
            fg="green",
            bg="black"
        )
        features_title.pack(anchor='w', pady=(0, 10))

        text_font = tkfont.Font(family="Arial", size=12)
        features_text = """
⏰ Flexible timer: 15min to 2 hours sessions / Timer linh hoạt: 15 phút đến 2 giờ
📝 Task management: Add, edit, complete tasks / Quản lý task: Thêm, sửa, hoàn thành
📊 Progress tracking: Session count & completion % / Theo dõi tiến độ: Đếm session & %
🔄 Auto-continue: Seamless session transitions / Tự động tiếp tục: Chuyển session mượt mà
🎵 Sound effects: Audio feedback (optional) / Hiệu ứng âm thanh: Phản hồi âm thanh
💾 Auto-save: All data saved automatically / Tự động lưu: Toàn bộ dữ liệu được lưu
        """.strip()
        
        features_label = tk.Label(
            parent,
            text=features_text,
            font=text_font,
            fg="white",
            bg="black",
            justify='left'
        )
        features_label.pack(anchor='w', pady=(0, 20))

    def create_bottom_buttons(self):
        """Tạo các nút ở dưới"""
        # Don't show again checkbox
        checkbox_frame = tk.Frame(self.root, bg='black')
        checkbox_frame.pack(pady=10)
        
        dont_show_cb = tk.Checkbutton(
            checkbox_frame,
            text="Don't show this again / Không hiển thị lại",
            variable=self.dont_show_again,
            fg="white",
            bg="black",
            selectcolor="black",
            font=tkfont.Font(family="Arial", size=10),
            command=self._on_checkbox_clicked
        )
        dont_show_cb.pack()

        button_frame = tk.Frame(self.root, bg='black')
        button_frame.pack(pady=10)

        btn_font = tkfont.Font(family="Arial", size=14, weight="bold")

        # Start button (only button)
        start_btn = tk.Button(
            button_frame,
            text="🚀 Bắt đầu sử dụng / Start Using Timer",
            font=btn_font,
            width=35,
            height=2,
            bg="green",
            fg="white",
            command=self.start_timer
        )
        start_btn.pack(pady=5)

        # Tips
        tips_font = tkfont.Font(family="Arial", size=9)
        tips_label = tk.Label(
            self.root,
            text="💡 Tip: For best results, try 25-minute Pomodoro sessions first!\n    Mẹo: Để có kết quả tốt nhất, hãy thử session Pomodoro 25 phút trước!",
            font=tips_font,
            fg="cyan",
            bg="black",
            justify='center'
        )
        tips_label.pack(pady=10)

    def _on_checkbox_clicked(self):
        """Xử lý click checkbox"""
        if self.play_sound:
            self.play_sound()

    def start_timer(self):
        """Chuyển sang main timer app"""
        if self.play_sound:
            self.play_sound()
        # Save setting if user checked "don't show again"
        if self.dont_show_again.get():
            mark_welcome_shown()
            
        self.root.destroy()
        if self.on_start_callback:
            self.on_start_callback()

def show_welcome_screen(on_start_callback):
    """Show welcome screen"""
    root = tk.Tk()
    welcome = WelcomeScreen(root, on_start_callback)
    
    # Tạo sound manager cho welcome screen
    try:
        from ..managers.sound_manager import SoundManager
        sound_manager = SoundManager()
        welcome.play_sound = sound_manager.play_main_button_sound
    except:
        # Nếu không thể import sound manager, bỏ qua
        pass
    
    root.mainloop()
