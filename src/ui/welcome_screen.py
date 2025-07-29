# -*- coding: utf-8 -*-
"""
Welcome Screen Module - Introduction to Pomodoro and usage guide
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
        """Setup welcome window"""
        self.root.title("Study Timer - Welcome")
        self.root.configure(bg='black')
        self.root.geometry("800x900")
        self.root.resizable(True, True)
        
        # Center window
        self.center_window()

    def center_window(self):
        """Center window on screen (cross-platform)"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        pos_x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        pos_y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

    def create_widgets(self):
        """Create widgets for welcome screen"""
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
            text="🕐 Study Timer",
            font=title_font,
            fg="white",
            bg="black"
        )
        title_label.pack(pady=(10, 5))

        # Subtitle
        subtitle_font = tkfont.Font(family="Arial", size=14)
        subtitle_label = tk.Label(
            self.root,
            text="Pomodoro Technique & Study Session Manager",
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
        """Create scrollable content"""
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
        """Create Pomodoro explanation section"""
        # Section title
        section_font = tkfont.Font(family="Arial", size=16, weight="bold")
        pomodoro_title = tk.Label(
            parent,
            text="🍅 What is Pomodoro Technique?",
            font=section_font,
            fg="yellow",
            bg="black"
        )
        pomodoro_title.pack(anchor='w', pady=(0, 10))

        # Pomodoro explanation
        text_font = tkfont.Font(family="Arial", size=12)
        pomodoro_text = """
• Work in focused 25-minute intervals called "Pomodoros"
• Take a 5-minute break after each Pomodoro
• After 4 Pomodoros, take a longer 15-30 minute break
• Helps maintain focus and prevent burnout
• Increases productivity and time awareness
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
        """Create how-to-use section"""
        section_font = tkfont.Font(family="Arial", size=16, weight="bold")
        howto_title = tk.Label(
            parent,
            text="🎮 How to Use This App",
            font=section_font,
            fg="orange",
            bg="black"
        )
        howto_title.pack(anchor='w', pady=(0, 10))

        text_font = tkfont.Font(family="Arial", size=12)
        howto_text = """
1. Choose session duration: 15min, 25min (Pomodoro), 45min, 1-2 hours
2. Set your daily session target (default: 8 sessions)
3. Add tasks you want to work on during sessions
4. Click START to begin your focused work session
5. Take breaks when the timer suggests (auto-break feature)
6. Complete tasks and track your progress
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
        """Create features section"""
        section_font = tkfont.Font(family="Arial", size=16, weight="bold")
        features_title = tk.Label(
            parent,
            text="✨ Key Features",
            font=section_font,
            fg="green",
            bg="black"
        )
        features_title.pack(anchor='w', pady=(0, 10))

        text_font = tkfont.Font(family="Arial", size=12)
        features_text = """
⏰ Flexible timer: 15min to 2 hours sessions
📝 Task management: Add, edit, complete tasks
📊 Progress tracking: Session count & completion %
🔄 Auto-continue: Seamless session transitions 
🎵 Sound effects: Audio feedback (optional)
💾 Auto-save: All data saved automatically
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
        """Create bottom buttons"""
        # Don't show again checkbox
        checkbox_frame = tk.Frame(self.root, bg='black')
        checkbox_frame.pack(pady=10)
        
        dont_show_cb = tk.Checkbutton(
            checkbox_frame,
            text="Don't show this again",
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
            text="🚀 Start Using Timer",
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
            text="💡 Tip: For best results, try 25-minute Pomodoro sessions first!",
            font=tips_font,
            fg="cyan",
            bg="black",
            justify='center'
        )
        tips_label.pack(pady=10)

    def _on_checkbox_clicked(self):
        """Handle checkbox click"""
        if self.play_sound:
            self.play_sound()

    def start_timer(self):
        """Start main timer app"""
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
    
    # Create sound manager for welcome screen
    try:
        from ..managers.sound_manager import SoundManager
        sound_manager = SoundManager()
        welcome.play_sound = sound_manager.play_main_button_sound
    except:
        # If can't import sound manager, skip
        pass
    
    root.mainloop()
