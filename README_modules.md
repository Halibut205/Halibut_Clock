# Fliqlo Timer - Modular Version

Ứng dụng đồng hồ bấm giờ với giao diện kiểu Fliqlo, được tái cấu trúc thành các module riêng biệt.

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

## Cách chạy

### Chạy version mới (modular):
```bash
python main.py
```

### Chạy version cũ:
```bash
python fliqlo_timer.py
```

## Tính năng

- ⏰ Timer chính với định dạng HH:MM:SS
- ⏸️ Break timer tự động khi pause
- 🔄 Resume break timer từ thời điểm freeze
- 🎨 Giao diện Fliqlo-style (đen, trắng, xanh cyan)
- 🚀 Dễ dàng mở rộng và bảo trì

## Ưu điểm của cấu trúc mới

1. **Separation of Concerns**: Mỗi module có trách nhiệm riêng
2. **Maintainability**: Dễ bảo trì và debug
3. **Extensibility**: Dễ thêm tính năng mới
4. **Testability**: Có thể test từng module riêng biệt
5. **Reusability**: Có thể tái sử dụng components

## Mở rộng tính năng

Để thêm tính năng mới:
- **UI mới**: Thêm vào `ui_components.py`
- **Logic mới**: Thêm vào `timer_core.py` 
- **Kết nối**: Cập nhật `timer_controller.py`
