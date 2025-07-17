# 🕐 Fliqlo Timer - Pomodoro Study Timer

A **beautiful Pomodoro app** to help you focus on studying and working efficiently. Features **continuous timing system** for flexible time management, task tracking, cross-platform sound support, and **advanced data visualization with separated charts**.

![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

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
- **🚀 Unlimited Sessions**: Continue beyond your daily target (e.g., 9/8, 10/8 sessions)
- **🧠 Dynamic Session Goals**: Daily session targets adapt based on your monthly average + 2
- **⏰ Dynamic Study Goals**: Daily study time targets adapt based on your monthly average
- Session completion notifications with sound alerts
- Progress tracking with visual indicators
- **Extra Mode**: Special motivational messages when exceeding targets

### **📋 Task Management**
- Add tasks for each session
- Mark tasks as completed
- Reactivate completed tasks with the "↩ Undo" button
- Track your productivity across multiple sessions
- Clear completed tasks when needed

### **📊 Advanced Data Visualization**
- **Separated Charts**: Daily Sessions and Tasks in dedicated tabs
- **Study Time Analysis**: Combined study time and break time trends
- **Efficiency Tracking**: Dual y-axis charts with performance zones
- **Goal Progress**: Visual progress indicators with adaptive target lines
- **Dynamic Targets**: Session goals automatically adjust based on your performance
- **Professional Styling**: Enhanced matplotlib charts with beautiful design
- **Export Functionality**: Save charts as high-quality PNG files

### **📈 Statistics Dashboard**
- **Daily Stats**: Track study time, sessions, tasks, and efficiency
- **Weekly Overview**: 7-day performance analysis with visual indicators
- **Monthly Trends**: Long-term progress tracking and goal achievement
- **Performance Zones**: Color-coded productivity levels
- **Achievement Badges**: Unlock rewards based on your productivity

### **🎵 Audio Experience**
- **Smart Sound System**: Session completion alerts
- **Background Music**: Optional focus-enhancing audio
- **Cross-Platform Support**: Works on Windows, macOS, and Linux
- **Customizable Audio**: Easy to replace with your own sound files

---

## 🚀 Quick Start

### **Windows Users**
```bash
# Double-click to install and run:
setup.bat    # Install dependencies
run.bat      # Launch the application
```

### **macOS/Linux Users**
```bash
# Make scripts executable and run:
chmod +x setup.sh run.sh
./setup.sh   # Install dependencies  
./run.sh     # Launch the application
```

### **Manual Installation**
```bash
# Clone the repository
git clone https://github.com/Halibut205/Study_Fliqlo_Clock.git
cd Study_Fliqlo_Clock

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

---

## 📸 Screenshots

### Main Timer Interface
- Clean, modern design with dual timer system
- Real-time session progress tracking
- Easy-to-use controls for start/pause/reset

### Task Management
- Add and track tasks for each study session
- Visual completion indicators
- Flexible task reactivation system

### Statistics Dashboard
- **Study Time Chart**: Track daily study and break patterns
- **Sessions Chart**: Monitor daily session completion
- **Tasks Chart**: Visualize task completion trends  
- **Efficiency Analysis**: Performance tracking with dual y-axis display

### Chart Features
- Professional matplotlib styling
- Separated tabs for better data organization
- Export functionality for reports and presentations
- Performance zones and target lines
- **Dynamic Goals**: Automatically adapting session targets

---

## 🧠 Smart Features

### **Dynamic Goals System**
The timer intelligently adapts both your daily session and study time goals based on your performance:

#### **📊 Dynamic Session Goals**
- **Calculation**: Monthly average sessions + 2
- **Range**: 3-12 sessions (minimum-maximum)
- **Default**: 6 sessions for new users
- **Example**: If you average 5 sessions/day this month, your goal becomes 7 sessions

#### **⏰ Dynamic Study Time Goals**  
- **Calculation**: Monthly average study hours
- **Range**: 2-8 hours (minimum-maximum)
- **Default**: 4 hours for new users
- **Example**: If you average 3.5 hours/day this month, your goal becomes 3.5 hours

This ensures your goals are:
- ✅ **Realistic**: Based on your actual performance history
- ✅ **Personalized**: Adapts to your unique study patterns
- ✅ **Adaptive**: Automatically adjusts as you improve
- ✅ **Motivating**: Encourages steady, sustainable progress

---

## ⚙️ Configuration

### **Timer Settings**
- **Session Duration**: 15, 20, 25, 30, 45, 60, 90, or 120 minutes
- **Target Sessions**: 1-20 sessions per day (or use dynamic goals)
- **Sound Alerts**: Enable/disable session completion sounds

### **Statistics Settings**
- **Chart Display**: Toggle between different chart views
- **Export Options**: Save charts as PNG files
- **Data Management**: Reset daily stats or export data

### **Audio Settings**
- **Sound Files**: Located in `sfx/` directory
- **Volume Control**: System volume controls
- **Custom Sounds**: Replace default files with your own

---

## 🛠️ Requirements

- **Python**: 3.8 or higher
- **Dependencies**: 
  - `pygame` (for audio support)
  - `matplotlib>=3.5.0` (for advanced charts)
  - `tkinter` (usually included with Python)
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
│
├── src/                 # Source code
│   ├── core/           # Timer logic
│   │   ├── timer_core.py         # Dual clock system
│   │   └── timer_controller.py   # Main controller
│   ├── ui/             # User interface  
│   │   ├── ui_components.py      # Main UI
│   │   ├── task_ui.py           # Task management UI
│   │   └── daily_stats_window.py # Statistics UI with separated charts
│   └── managers/       # Business logic
│       ├── sound_manager.py      # Audio management
│       ├── task_manager.py       # Task tracking
│       └── daily_stats_manager.py # Statistics tracking
│
├── tests/              # Test files
│   ├── test_*.py              # Unit tests
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

## 🆕 Recent Updates

### **v2.1 - Dynamic Goals System**
- ✅ **Smart Session Targets**: Daily session goals adapt to your monthly performance (avg + 2)
- ✅ **Dynamic Study Goals**: Daily study time goals based on your monthly average
- ✅ **Adaptive Charts**: All target lines automatically adjust to your habits
- ✅ **Performance-Based**: Goals range from 3-12 sessions and 2-8 hours
- ✅ **Intelligent Defaults**: New users start with 6 sessions and 4 hours goals

### **v2.0 - Advanced Charts & Separated Views**
- ✅ **Separated Charts**: Daily Sessions and Tasks now in dedicated tabs
- ✅ **Enhanced Styling**: Professional matplotlib styling with beautiful design
- ✅ **Performance Zones**: Color-coded productivity levels in charts
- ✅ **Export Functionality**: Save charts as high-quality PNG files
- ✅ **Efficiency Tracking**: Dual y-axis charts with transparency fixes
- ✅ **Target Lines**: Visual goal indicators for sessions and tasks

### **Chart Improvements**
- **Study Time Chart**: Combined study/break analysis with goal tracking
- **Sessions Chart**: Dedicated tab with 6 sessions/day target line
- **Tasks Chart**: Separate visualization with 8 tasks/day target
- **Efficiency Chart**: Dual y-axis with study efficiency and goal progress

---

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

### **Development Setup**
```bash
# Clone and setup development environment
git clone https://github.com/Halibut205/Study_Fliqlo_Clock.git
cd Study_Fliqlo_Clock
pip install -r requirements.txt

# Run tests
python tests/test_daily_stats.py
python tests/test_enhanced_charts.py
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Fliqlo**: Inspiration for the clean, minimalist timer design
- **Pomodoro Technique**: Time management methodology
- **Matplotlib**: Advanced charting and visualization library
- **Python Community**: For the excellent libraries and tools

---

**Start your productive study sessions today!** 🚀📚
