# 🕐 Fliqlo Study Timer

Ứng dụng đếm thời gian học tập với giao diện Fliqlo-style, quản lý session và task management tích hợp của Halibut.

---

## 🚀 Hướng dẫn sử dụng

### 📥 Cài đặt và chạy

#### **Windows:**
1. Tải mã nguồn:  
    ```bash
    git clone <repo_url>
    cd Timer
    ```
2. Nhấp đúp `setup.bat` để cài đặt.
3. Nhấp đúp `run.bat` để chạy ứng dụng.

#### **Linux/Mac:**
1. Tải mã nguồn:  
    ```bash
    git clone <repo_url>
    cd Timer
    ```
2. Chạy lệnh:  
    ```bash
    chmod +x setup.sh && ./setup.sh
    chmod +x run.sh && ./run.sh
    ```

#### **Dành cho lập trình viên:**
- Chạy trực tiếp:  
  ```bash
  python main.py
  ```

### 🔄 Sử dụng hàng ngày
- **Windows:** Nhấp đúp `run.bat`
- **Linux/Mac:** `./run.sh` hoặc `python3 main.py`

---

## 📋 Tính năng

### ⏰ **Timer Features**
- Đếm thời gian count-up (HH:MM:SS)
- **Điều chỉnh thời lượng session:** 15min, 25min, 30min, 45min, 1h, 1.5h, 2h
- Session management với auto-break (5min break sau mỗi session)
- Tự động chuyển session/break
- Đặt mục tiêu số session/ngày
- Theo dõi tiến độ session (%)

### 📝 **Task Management**
- Thêm/sửa/xóa/hoàn thành tasks
- Đánh dấu độ ưu tiên
- Task summary và statistics
- Tự động lưu vào JSON
- Task UI compact và dễ sử dụng

### 🎨 **UI/UX**
- **Welcome screen:** Interactive Pomodoro tutorial song ngữ (English-Vietnamese)
- **Bilingual support:** Giao diện và hướng dẫn Anh-Việt
- **Credit:** "Created by Halibut" hiển thị trong welcome screen
- Giao diện Fliqlo-style (đen, trắng, cyan)
- Nút điều khiển lớn, dễ bấm
- Thiết kế compact (500x600px)
- Help button (❓) để xem lại hướng dẫn
- Sound effects (optional)

---

## 📁 Cấu trúc dự án

```
Timer/
├── main.py              # Entry point chính
├── config.py            # Cấu hình tập trung
├── requirements.txt     # Dependencies
├── README.md            # File này
├── run.bat/.sh          # Scripts chạy
├── setup.bat/.sh        # Scripts cài đặt
├── .gitignore           # Git ignore
├── src/                 # Source code
│   ├── core/           # Timer logic
│   │   ├── timer_core.py
│   │   └── timer_controller.py
│   ├── ui/             # UI components
│   │   ├── ui_components.py
│   │   └── task_ui.py
│   └── managers/       # Managers
│       ├── sound_manager.py
│       └── task_manager.py
├── data/               # Data persistence
│   ├── tasks_data.json # Task storage
│   ├── app_settings.json # App preferences
│   └── README.md
└── sfx/                # Sound effects
    ├── button_1.mp3    # Click sound
    └── README.md
```

---

## 🎮 Hướng dẫn sử dụng

### **Timer Controls:**
- **▶️ Start:** Bắt đầu đếm thời gian
- **⏸️ Pause:** Tạm dừng (auto-break timer)
- **⏹️ Stop:** Dừng và reset về 0
- **🔄 Resume:** Tiếp tục từ break
- **❓ Help:** Xem lại hướng dẫn Pomodoro

### **Task Management:**
1. **Thêm task:** Nhập vào ô → nhấn "Add" hoặc Enter
2. **Hoàn thành:** Chọn task → nhấn "✓"
3. **Chỉnh sửa:** Chọn task → nhấn "✏️"
4. **Xóa:** Chọn task → nhấn "🗑️"
5. **Clear done:** Xóa tất cả tasks đã hoàn thành

### **Session Management:**
- **Điều chỉnh thời lượng:** Chọn từ dropdown (15min - 2h)
- **Pomodoro mode:** Chọn 25min cho phương pháp Pomodoro chuẩn
- **Study mode:** Chọn 45min - 2h cho session học dài hạn
- Auto-continue giữa các session
- Target sessions có thể điều chỉnh
- Progress bar hiển thị tiến độ session hiện tại

---

## ⚙️ Technical Details

### **Dependencies:**
- Python 3.8+
- tkinter (built-in)
- pygame (optional, for sound)

### **Data Storage:**
- Tasks: `data/tasks_data.json`
- Config: `config.py`
- Sound: `sfx/button_1.mp3`

### **Cross-platform:**
- Windows: `.bat` scripts
- Linux/Mac: `.sh` scripts
- Pure Python compatibility

---

## 🔧 Development

### **Module Structure:**
- `src.core`: Timer logic và controller
- `src.ui`: UI components và task UI
- `src.managers`: Sound và task managers
- `config.py`: Centralized settings

### **Key Features:**
- Modular architecture
- Clean separation of concerns
- Easy to extend and maintain
- Graceful fallbacks (sound, data)

---

## � Support

Nếu gặp vấn đề:
1. Kiểm tra Python version (3.8+)
2. Chạy `setup.bat/.sh` lại
3. Kiểm tra file `data/tasks_data.json` tự tạo
4. Nếu thiếu sound: `pip install pygame`

---

**🎯Halibut** 🚀

