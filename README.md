# Study Fliqlo Clock

Đây là project linh tinh làm đồng hồ kiểu Fliqlo bằng Python/Tkinter/…

## 🚀 Cách chạy

1. Clone repo hoặc tải source
2. Chạy file bash
3. Học 10 tiếng 1 ngày nhé

## 📋 Mô tả

Ứng dụng đếm tăng thời gian (count-up timer) với giao diện nền đen, chữ trắng lớn.

## Cấu trúc Project

```
Timer/
├── main.py                 # Entry point của ứng dụng
├── timer_controller.py     # Controller điều phối giữa UI và Logic
├── timer_core.py          # Core logic của timer
├── ui_components.py       # UI components và widgets
├── fliqlo_timer.py        # File gốc (legacy)
├── fliqlo_timer_runner.bat # Batch file để chạy
└── README.md              # File này
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

### 4. `main.py` - Main Application
- Entry point của ứng dụng
- Khởi tạo và chạy app

## ✅ Tính năng (Đang update)

- Nút Start, Pause, Resume, Reset
- Có count thời gian break

## 💻 Yêu cầu

- Python 3.8 trở lên
- Tkinter
