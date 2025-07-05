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
├── task_manager.py           # Quản lý tasks và tiến độ
├── task_ui.py               # UI components cho task management
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

### 6. `task_manager.py` - Task Management
- Quản lý tasks (thêm, sửa, xóa, hoàn thành)
- Lưu trữ persistent vào JSON file
- Priority system và task statistics
- Session-based task assignment

### 7. `task_ui.py` - Task UI Components
- Giao diện quản lý tasks
- Listbox hiển thị active và completed tasks
- Buttons cho các thao tác task
- Task summary và progress display

### 8. `main.py` - Main Application
- Entry point của ứng dụng
- Khởi tạo và chạy app

## ✅ Tính năng (Đang update)

- ⏰ Timer chính với định dạng HH:MM:SS
- 📚 **Session Management**: Đếm sessions (mỗi session = 1 giờ)
- 🎯 **Target Sessions**: Thiết lập số session muốn hoàn thành trong ngày (1-20)
- 🔄 **Auto Continue**: Tự động tiếp tục session tiếp theo hoặc dừng để break
- 📊 **Progress Tracking**: Hiển thị tiến độ session hiện tại (%)
- 📝 **Task Management**: Thêm, sửa, xóa, hoàn thành tasks
- ✅ **Task Tracking**: Theo dõi tasks đã hoàn thành và còn lại
- 🎨 **Priority System**: Đánh dấu độ ưu tiên tasks (cao, bình thường, thấp)
- 💾 **Auto Save**: Tự động lưu tasks vào file JSON
- 📈 **Task Statistics**: Hiển thị tỷ lệ hoàn thành tasks
- ⏸️ Break timer tự động khi pause  
- 🔄 Resume break timer từ thời điểm freeze
- 🎨 Giao diện Fliqlo-style (đen, trắng, xanh cyan, vàng, cam)
- 🔊 Âm thanh SFX khi bấm nút (button_1.mp3)
- 🎛️ Bật/tắt âm thanh
- 🚀 Dễ dàng mở rộng và bảo trì

## 💻 Yêu cầu

- Python 3.8 trở lên
- Tkinter (có sẵn với Python)
- Pygame (cho âm thanh)
- File âm thanh `button_1.mp3` trong thư mục `sfx/`

## 🎮 Hướng dẫn sử dụng Task Management:

### **Thêm Task:**
1. Nhập task vào ô "New Task"
2. Nhấn "Add Task" hoặc Enter
3. Task sẽ xuất hiện trong danh sách "Active Tasks"

### **Hoàn thành Task:**
1. Chọn task trong danh sách "Active Tasks"
2. Nhấn "✓ Complete"
3. Task chuyển sang "Completed Tasks"

### **Chỉnh sửa Task:**
1. Chọn task cần sửa
2. Nhấn "✏️ Edit"
3. Nhập nội dung mới trong dialog

### **Xóa Task:**
1. Chọn task cần xóa
2. Nhấn "🗑️ Delete"
3. Xác nhận xóa

### **Quản lý:**
- Tasks tự động lưu vào file `tasks_data.json`
- Có thể xóa tất cả completed tasks bằng "🧹 Clear All"
- Task summary hiển thị tổng quan tiến độ
