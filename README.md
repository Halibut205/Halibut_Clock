# Study Fliqlo Clock

Đây là project linh tinh làm đồng hồ kiểu Fliqlo bằng Python/Tkinter/…

## 🚀 Cách chạy

1. Clone repo hoặc tải source
2. Cài pygame: Chạy `install_dependencies.bat` hoặc `pip install pygame`
3. Đặt file âm thanh `button_1.mp3` vào thư mục `sfx/`
4. Chạy file `fliqlo_timer_runner.bat`
5. Học 10 tiếng 1 ngày nhé

## 📋 Mô tả

Ứng dụng đếm tăng thời gian (count-up timer) với giao diện nền đen, chữ trắng lớn.

## Cấu trúc Project

```
Timer/
├── main.py                    # Entry point của ứng dụng
├── timer_controller.py        # Controller điều phối giữa UI và Logic
├── timer_core.py             # Core logic của timer
├── ui_components.py          # UI components và widgets
├── sound_manager.py          # Quản lý âm thanh và SFX
├── sfx/                      # Thư mục chứa file âm thanh
│   ├── button_1.mp3         # Âm thanh khi bấm nút (cần tự thêm)
│   └── README.md            # Hướng dẫn về âm thanh
├── fliqlo_timer.py          # File gốc (legacy)
├── fliqlo_timer_runner.bat  # Batch file để chạy
├── install_dependencies.bat # Script cài pygame
├── requirements.txt         # Dependencies
└── README.md               # File này
```

## Các Module

### 1. `timer_core.py` - Timer Core Logic
- Quản lý trạng thái timer chính và break timer
- Logic đếm thời gian
- Format thời gian
- Callbacks cho UI updates

### 2. `ui_components.py` - UI Components
- Tạo và quản lý giao diện người dùng
- Các widget: labels, buttons
- Styling và layout
- Event handlers cho UI

### 3. `timer_controller.py` - Controller
- Điều phối giữa UI và Core Logic
- Xử lý user interactions
- Update loop chính
- API cho các tính năng mở rộng

### 5. `sound_manager.py` - Sound Effects
- Quản lý âm thanh cho ứng dụng
- Phát âm thanh khi bấm nút
- Hỗ trợ bật/tắt âm thanh
- Điều chỉnh âm lượng

### 6. `main.py` - Main Application
- Entry point của ứng dụng
- Khởi tạo và chạy app

## ✅ Tính năng (Đang update)

- ⏰ Timer chính với định dạng HH:MM:SS
- ⏸️ Break timer tự động khi pause  
- 🔄 Resume break timer từ thời điểm freeze
- 🎨 Giao diện Fliqlo-style (đen, trắng, xanh cyan)
- 🔊 Âm thanh SFX khi bấm nút (button_1.mp3)
- 🎛️ Bật/tắt âm thanh
- 🚀 Dễ dàng mở rộng và bảo trì

## 💻 Yêu cầu

- Python 3.8 trở lên
- Tkinter (có sẵn với Python)
- Pygame (cho âm thanh)
- File âm thanh `button_1.mp3` trong thư mục `sfx/`
