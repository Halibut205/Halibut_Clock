# 🕐 Fliqlo Timer - Pomodoro Study Timer

A **beautiful bilingual Pomodoro app** to help you focus on studying and working efficiently. Modern interface, task management, and background music support.

---

## ✨ Features

### 🎯 **Core Timer Functions**
- **Pomodoro Timer**: 25-minute focus sessions with 5-minute breaks
- **Flexible Duration**: 15min, 25min, 30min, 45min, 1hr, 1.5hr, 2hr options
- **Session Tracking**: Progress counter (e.g., Session: 3/8)
- **Auto Continue**: Automatic break ↔ session transitions
- **Session Reset**: Reset progress counter anytime

### 📋 **Task Management**
- **Add Tasks**: Create tasks for specific sessions
- **Priority Levels**: 🔴 High, 🟡 Medium, 🟢 Low priority
- **Task Progress**: Mark tasks as completed
- **Active & Completed**: Separate lists for organization
- **Task Editing**: Modify task text anytime

### 🔊 **Background Music System**
- **Whitenoise Support**: Automatic background music during sessions
- **Smart Controls**: Music starts/pauses/stops with timer
- **Loop Playback**: Continuous background audio
- **Button Sounds**: Audio feedback for all interactions

### 🌍 **Bilingual Interface**
- **Vietnamese + English**: Dual language support
- **Welcome Screen**: Professional onboarding experience
- **Help System**: Built-in usage instructions

---

## 🙏 Credits

- **Pomodoro Technique**: Inspired by Francesco Cirillo's time management method.
- **Fliqlo Design**: Inspired by the iconic flip clock screensaver.
- **Halibut**: Special thanks for the original idea and contributions.

---

## 📁 Project Structure

```
Timer/
├── main.py              # Main application entry point
├── config.py            # Application configuration  
├── requirements.txt     # Dependencies (pygame)
├── run.bat/.sh          # Launch scripts
├── setup.bat/.sh        # Installation scripts
│
├── src/                 # Source code
│   ├── core/           # Timer logic
│   │   ├── timer_core.py      # Timer engine
│   │   └── timer_controller.py # Main controller
│   │
│   ├── ui/             # User interface
│   │   ├── ui_components.py   # Main UI components
│   │   ├── task_ui.py         # Task management UI
│   │   ├── welcome_screen.py  # Bilingual welcome screen
│   │   └── app_settings.py    # Application settings
│   │
│   └── managers/       # Business logic
│       ├── sound_manager.py   # Audio system
│       └── task_manager.py    # Task management
│
├── sfx/                # Sound effects
│   ├── button_1.mp3          # Button click sounds
│   └── whitenoise_1.mp3      # Background music
│
└── data/               # User data
    ├── tasks_data.json       # Saved tasks
    └── app_settings.json     # User preferences
```

---

## 🚀 Quick Start

### **Windows**
1. Download the ZIP file from the project's GitHub page.
2. Extract the ZIP file to your desired folder.
3. Double-click `setup.bat` to install the required components.
4. Once installation is complete, double-click `run.bat` to launch the application.

### **macOS/Linux**
1. Download the source code from the project's GitHub page using the command:
    ```bash
    git clone https://github.com/your-username/fliqlo-timer.git
    ```
2. Open the project directory:
    ```bash
    cd fliqlo-timer
    ```
3. Right-click the `setup.sh` file and select **Properties**. Under the **Permissions** tab, check **Allow executing file as program**.
4. Double-click `setup.sh` to install the required components.
5. After installation, double-click `run.sh` to launch the application.

---

![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-green)
![License](https://img.shields.io/badge/license-MIT-yellow)
