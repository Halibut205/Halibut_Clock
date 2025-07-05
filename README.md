# Study Fliqlo Clock

Đây là đồng hồ count-up (tăng thời gian) bằng Python/Tkinter của Halibut.

---

## 🚀 Hướng dẫn chạy ứng dụng

### 1. Cài đặt lần đầu

#### **Windows**
1. Clone repo theo cách của bạn:  
    ```bash
    git clone <repo_url>
    ```
2. Cài đặt: Double-click `setup.bat`
3. Chạy app: Double-click `run.bat`

#### **Linux/Mac**
1. Clone repo theo cách của bạn:    
    ```bash
    git clone <repo_url>
    ```
2. Cài đặt:  
    ```bash
    chmod +x setup.sh && ./setup.sh
    ```
3. Chạy app:  
    ```bash
    chmod +x run.sh && ./run.sh
    ```
    hoặc  
    ```bash
    python3 main.py
    ```

### 2. Chạy hàng ngày

- **Windows:** Double-click `run.bat`
- **Linux/Mac:** `./run.sh` hoặc `python3 main.py`

### 3. Nếu ngựa ngựa

dùng Python:  
```bash
python main.py
```

### 4. Yêu cầu

- Python 3.8 trở lên
- Tkinter (thường có sẵn với Python)
- Pygame (setup script sẽ tự cài)

---

## 📝 Mô tả ứng dụng

- Đếm thời gian dạng count-up với giao diện nhỏ gọn, nền đen, chữ trắng lớn.
- Nút bấm to, dễ thao tác.
- Tích hợp quản lý tasks.

---

## 📁 Cấu trúc thư mục

<details>
<summary>Xem chi tiết</summary>

```
Timer/
├── main.py                  # Entry point
├── config.py                # Cấu hình
├── requirements.txt         # Dependencies
├── README.md                # File này
├── src/
│   ├── core/
│   │   ├── timer_core.py
│   │   └── timer_controller.py
│   ├── ui/
│   │   ├── ui_components.py
│   │   └── task_ui.py
│   └── managers/
│       ├── sound_manager.py
│       └── task_manager.py
├── data/
│   └── tasks_data.json      # Lưu tasks
├── sfx/
│   ├── button_1.mp3         # Âm thanh (thêm thủ công)
│   └── README.md
├── assets/
├── scripts/
│   ├── fliqlo_timer_runner.bat
│   └── install_dependencies.bat
└── __pycache__/
```
</details>

---

## 🧩 Các module chính

- **Core:**  
  `timer_core.py` (logic timer), `timer_controller.py` (điều phối)
- **UI:**  
  `ui_components.py` (giao diện chính), `task_ui.py` (quản lý task)
- **Managers:**  
  `sound_manager.py` (âm thanh), `task_manager.py` (quản lý task)
- **Khác:**  
  `config.py` (cấu hình), `main.py` (khởi động app), `data/`, `sfx/`, `assets/`, `scripts/`

---

## ✅ Tính năng nổi bật

- ⏰ Đếm thời gian dạng HH:MM:SS
- 📚 Quản lý session (mỗi session = 1 giờ)
- 🎯 Đặt mục tiêu số session/ngày
- 🔄 Tự động chuyển session/break
- 📊 Theo dõi tiến độ session (%)
- 📝 Quản lý tasks: thêm, sửa, xóa, hoàn thành
- ✅ Theo dõi tasks đã hoàn thành/còn lại
- 🎨 Đánh dấu độ ưu tiên task
- 💾 Tự động lưu tasks vào JSON
- 📈 Thống kê tasks
- ⏸️ Break timer tự động khi pause
- 🔄 Resume break timer
- 🎨 Giao diện Fliqlo-style (đen, trắng, cyan, vàng, cam)
- 🖱️ Nút điều khiển to, có icon
- 📱 Thiết kế nhỏ gọn (500x600px)

---

## 🎮 Hướng dẫn quản lý Task

- **Thêm task:**  
  Nhập vào ô "Task:" → Nhấn "Add" hoặc Enter → Task sẽ vào danh sách "📋 Active"
- **Hoàn thành task:**  
  Chọn task → Nhấn "✓" → Task chuyển sang "✅ Done"
- **Chỉnh sửa/Xóa:**  
  Chọn task → Nhấn "✏️" (sửa) hoặc "🗑️" (xóa)
- **Quản lý:**  
  - Tasks tự động lưu vào `data/tasks_data.json`
  - Nhấn "Clear" để xóa tất cả completed tasks
  - Task summary hiển thị tiến độ

---

## 🔧 Ưu điểm cấu trúc

- **Phân chia module rõ ràng:** UI, logic, data tách biệt
- **Dễ bảo trì, mở rộng**
- **Import rõ ràng, organized**
- **Cấu hình tập trung**
- **Quản lý data riêng biệt**
- **Scripts tiện dụng**

