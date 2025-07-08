# 🕐 Fliqlo Timer - Pomodoro Study Timer

A **beautiful Pomodoro app** to help you focus on studying and working efficiently. Features **continuous timing system** for flexible time management, task tracking, and cross-platform sound support.

---

## ✨ Features

### **🕐 Dual Clock System**
- **Main Timer**: Continuously tracks your total work time (never resets)
- **Break Timer**: Tracks your break/pause time  
- **Smart Toggle**: Seamlessly switch between work and break modes
- **Independent Timing**: Each clock preserves its state when paused

### **⏱️ How It Works**
1. **START**: Main timer runs continuously, break timer freezes
2. **PAUSE**: Main timer freezes (preserves time), break timer starts running  
3. **RESUME**: Break timer freezes, main timer continues from where it left off
4. **Session Complete**: Every 15/25/30 minutes (configurable), notification sound plays
5. **User Choice**: Choose to continue working or take a longer break
6. **Continuous Progress**: Main timer never resets - tracks total work time across all sessions

### **🎯 Smart Session Management**
- Customizable session duration (15 min to 2 hours)
- Flexible target sessions (1-20 sessions)
- Session completion notifications with sound alerts
- Progress tracking with visual indicators

### **📋 Task Management**
- Add tasks for each session
- Mark tasks as completed
- Reactivate completed tasks with the "↩ Undo" button
- Track your productivity across multiple sessions
- Clear completed tasks when needed

### **📊 Enhanced Daily Statistics**
- **Access**: Click the "📊 Daily Stats" button on the main interface
- **Separate Window**: Opens a dedicated statistics window with multiple tabs:
  - **📅 Today Tab**: Current day's study time, break time, sessions, and tasks with:
    - **Progress Cards**: Visual stat cards with trend indicators vs yesterday
    - **Progress Bars**: Mini progress bars showing daily goal completion
    - **Visual Indicators**: Color-coded efficiency meters and emoji feedback
    - **Motivational Messages**: Dynamic encouragement based on your progress
    - **Achievement Badges**: Unlock badges for study milestones (Goal Master, Focus Champion, etc.)
    - **Enhanced Summary**: Study efficiency, session averages, and goal tracking
  - **📊 Weekly Tab**: 7-day overview with enhanced daily breakdown table featuring:
    - **Color-coded rows**: Today highlighted, high productivity days marked
    - **Visual indicators**: Emoji badges for performance levels (🔥 4h+, 💪 2h+, ⏱️ 1h+)
    - **Efficiency tracking**: Study vs break time ratios
  - **📅 Monthly Tab**: Complete month statistics with:
    - **Month Selector**: Choose any of the last 12 months to view
    - **Enhanced Cards**: Shadow effects and gradient styling for monthly stats
    - **Top 5 Study Days**: Best performing days with detailed breakdown
    - **3-Month Comparison**: Visual comparison with productivity trends
  - **📈 Charts Tab**: ASCII-based mini charts and visual progress tracking
- **Visual Enhancements**:
  - **Material Design**: Modern card-based interface with clean styling
  - **Color Coding**: Performance-based colors (Green: Excellent, Orange: Good, Red: Improve)
  - **Progress Indicators**: Real-time progress bars and visual feedback
  - **Trend Analysis**: Compare current performance with previous periods
  - **ASCII Charts**: Simple but effective visual trends for session data
- **Real-time Updates**: Statistics update automatically as you study
- **Data Export**: Export your statistics data to JSON format
- **Reset Option**: Reset today's statistics if needed
- **Persistent Storage**: All data saved to `data/daily_stats.json`

### **🔊 Audio System**
- Button click sounds for feedback
- Background white noise during work sessions
- Session completion alert (rang.mp3)
- Automatic audio management (pause during breaks)

---

##  Quick Start

### **Windows**
1. Download the ZIP file or clone this repository
2. Extract to your desired folder
3. Double-click `setup.bat` to install dependencies
4. Double-click `run.bat` to launch the application

**Note**: Use `run_debug.bat` for debug output, or `run_silent.vbs` for completely silent operation.

### **macOS/Linux**
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/fliqlo-timer.git
    cd fliqlo-timer
    ```
2. Make setup script executable and run:
    ```bash
    chmod +x setup.sh
    ./setup.sh
    ```
3. Launch the application:
    ```bash
    ./run.sh
    ```

---

## 🎮 How to Use

### **Basic Operation**
1. **Set Session Duration**: Choose from 15 minutes to 2 hours
2. **Set Target Sessions**: Choose how many sessions you want to complete (1-20)
3. **Click START**: Timer begins counting, break timer stays at 00:00:00
4. **Click PAUSE**: Timer freezes (preserves current time), break timer starts
5. **Click RESUME**: Break timer freezes, main timer continues from previous time
6. **Session Complete**: Hear the notification sound and choose your next action

### **Session Management**
- When a session completes, you'll hear **rang.mp3** notification
- Choose **YES** to start the next session immediately
- Choose **NO** to take a break (break timer will run)
- Complete all sessions to receive a congratulatory message

### **Task Management**
- Add tasks for each session using the task panel
- Mark tasks as completed when finished
- Reactivate completed tasks with the "↩ Undo" button
- Track your productivity across multiple sessions
- Clear completed tasks when needed

---

## 🛠️ Technical Requirements

- **Python**: 3.8 or higher
- **Dependencies**: pygame (for audio)
- **Platform**: Windows, macOS, Linux
- **Audio Files**: Included in `sfx/` directory

---

## 📁 Project Structure

```
Timer/
├── main.py              # Application entry point
├── config.py            # Configuration settings  
├── requirements.txt     # Python dependencies
├── run.bat/.sh          # Launch scripts
├── setup.bat/.sh        # Installation scripts
├── LICENSE              # MIT License
├── CHANGELOG.md         # Version history
│
├── src/                 # Source code
│   ├── core/           # Timer logic
│   │   ├── timer_core.py         # Dual clock system
│   │   └── timer_controller.py   # Main controller
│   ├── ui/             # User interface  
│   │   ├── ui_components.py      # Main UI
│   │   ├── task_ui.py           # Task management UI
│   │   └── daily_stats_window.py # Statistics UI
│   └── managers/       # Business logic
│       ├── sound_manager.py      # Audio management
│       ├── task_manager.py       # Task tracking
│       └── daily_stats_manager.py # Statistics tracking
│
├── tests/              # Test files and demos
│   ├── test_*.py              # Unit tests
│   ├── demo_*.py              # Demo scripts
│   └── README.md              # Test documentation
│
├── docs/               # Documentation
│   ├── ENHANCED_UI_FEATURES.md    # UI feature docs
│   └── README.md                  # Documentation overview
│
├── sfx/                # Sound effects
│   ├── button_1.mp3          # Button sounds
│   ├── whitenoise_1.mp3      # Background music
│   └── rang.mp3              # Session completion
│
└── data/               # User data (auto-created)
    ├── tasks_data.json       # Saved tasks
    ├── app_settings.json     # User preferences
    └── daily_stats.json      # Daily statistics
```

---

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

---

![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-green)
![License](https://img.shields.io/badge/license-MIT-yellow)
