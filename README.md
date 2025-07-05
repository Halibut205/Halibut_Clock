# 🕐 Fliqlo Timer - Đồng Hồ Pomodoro Học Tập Của Halibut

---

## 👨‍💻 Tác Giả

**Tác giả: Halibut**

Ối zồi ôi ối zồi ôi
Trình là gì mà là trình ai chấm
Anh chỉ biết làm ba mẹ tự hào
Xây căn nhà thật to
Ở một mình 2 tấm
Ối zồi ôi ối zồi ôi
Cứ lên mạng phán xét
Tưởng là mình oai lắm
Nhìn vào sự nghiệp anh
Thèm chảy nước miếng
Giống mấy thằng biến thái
Nó đang rình ai tắm

---

**Fliqlo Timer** là ứng dụng đồng hồ Pomodoro song ngữ, giao diện hiện đại, quản lý công việc và hỗ trợ âm thanh đa nền tảng. Lý tưởng cho học tập tập trung và theo dõi hiệu suất.

## ✨ Tính Năng Nổi Bật

### ⏰ **Hệ Thống Hẹn Giờ Thông Minh**
- **Thời gian linh hoạt**: 15, 25 (Pomodoro), 30, 45 phút, 1-2 giờ
- **Gợi ý nghỉ giải lao**: Đề xuất thời điểm nghỉ hợp lý
- **Theo dõi phiên học**: Đếm số lần và phần trăm hoàn thành
- **Tự động chuyển phiên**: Chuyển tiếp mượt mà giữa các phiên

### 📝 **Quản Lý Công Việc**
- **Thêm/sửa/xóa/hoàn thành**: Quản lý công việc dễ dàng
- **Ưu tiên công việc**: Sắp xếp theo mức độ quan trọng
- **Theo dõi tiến độ**: Thống kê hoàn thành trực quan
- **Tự động lưu**: Lưu dữ liệu vào file JSON

### 🎨 **Giao Diện Hiện Đại**
- **Phong cách Fliqlo**: Đen/trắng/xanh cyan sang trọng
- **Song ngữ**: Hỗ trợ tiếng Anh & Việt đầy đủ
- **Hướng dẫn chào mừng**: Giới thiệu Pomodoro dễ hiểu
- **Giao diện gọn nhẹ**: Cửa sổ 500x600px tối ưu
- **Trợ giúp tích hợp**: Nút ❓ hướng dẫn sử dụng

### 🔊 **Âm Thanh Đa Nền Tảng**
- **Tự động chọn âm thanh**: pygame → playsound → beep hệ thống
- **Tương thích mọi hệ điều hành**: Windows, macOS, Linux
- **Phát nền**: Âm thanh không làm gián đoạn ứng dụng
- **Không bắt buộc**: Ứng dụng vẫn chạy nếu thiếu âm thanh

---

## 🚀 Bắt Đầu Nhanh

### **Windows**
```bash
git clone https://github.com/your-username/fliqlo-timer.git
cd fliqlo-timer
setup.bat
run.bat
```

### **macOS/Linux**
```bash
git clone https://github.com/your-username/fliqlo-timer.git
cd fliqlo-timer
chmod +x setup.sh run.sh
./setup.sh
./run.sh
```

---

## 📁 Cấu Trúc Dự Án

```
Timer/
├── main.py              # Chương trình chính
├── config.py            # Cấu hình chung  
├── requirements.txt     # Thư viện âm thanh (tùy chọn)
├── run.bat/.sh          # Script chạy ứng dụng
├── setup.bat/.sh        # Script cài đặt
│
├── src/                 # Mã nguồn
│   ├── core/           # Logic hẹn giờ
│   │   ├── timer_core.py      # Bộ máy hẹn giờ
│   │   └── timer_controller.py # Điều khiển chính
│   │
│   ├── ui/             # Giao diện người dùng
│   │   ├── ui_components.py   # Thành phần giao diện
│   │   ├── task_ui.py         # Giao diện quản lý việc
│   │   ├── welcome_screen.py  # Màn hình chào mừng song ngữ
│   │   └── app_settings.py    # Cài đặt ứng dụng
│   │
│   └── managers/       # Quản lý hệ thống
│       ├── sound_manager.py   # Quản lý âm thanh
│       └── task_manager.py    # Lưu công việc
│
├── data/               # Dữ liệu người dùng (tự tạo)
│   └── *.json          # Cài đặt và công việc
│
└── sfx/                # Hiệu ứng âm thanh (tùy chọn)
    └── *.mp3           # File âm thanh
```

---

## 🎯 Hướng Dẫn Sử Dụng

### **Lần Đầu Sử Dụng**
1. **Màn hình chào mừng**: Hướng dẫn Pomodoro song ngữ
2. **Chọn thời gian**: Lựa chọn thời lượng phiên học  
3. **Thêm công việc**: Tạo danh sách việc cần làm
4. **Bắt đầu hẹn giờ**: Tập trung làm việc

### **Quy Trình Hàng Ngày**
1. **Đặt mục tiêu**: Chọn số phiên học/ngày (mặc định: 8)
2. **Lên kế hoạch**: Thêm công việc, đặt ưu tiên
3. **Làm việc tập trung**: Sử dụng hẹn giờ Pomodoro
4. **Nghỉ giải lao**: Làm theo gợi ý nghỉ tự động
5. **Theo dõi tiến độ**: Xem thống kê hoàn thành

---

## 🛠️ Thông Tin Kỹ Thuật

### **Phụ Thuộc**
- **Chính**: Python 3.8+ (có sẵn tkinter)
- **Âm thanh** (tùy chọn): pygame, playsound  
- **Lưu trữ**: File JSON (không cần database)

### **Ưu Tiên Âm Thanh**
1. **pygame** - Hiệu suất tốt, hỗ trợ nhiều định dạng
2. **playsound** - Tương thích đa nền tảng  
3. **Beep hệ thống** - Dự phòng

### **Hiệu Năng**
- **RAM**: ~30-50MB
- **CPU**: Rất nhẹ
- **Dung lượng**: <5MB

---

## 🌍 Hỗ Trợ Quốc Tế

- **Chào mừng song ngữ**: Màn hình giới thiệu Anh-Việt
- **Nội dung địa phương hóa**: Phù hợp văn hóa Việt
- **Hỗ trợ Unicode**: Hiển thị tiếng Việt chuẩn
- **Trợ giúp đa ngôn ngữ**: Hướng dẫn sử dụng song ngữ

---

## 🤝 Đóng Góp

```bash
git clone https://github.com/your-username/fliqlo-timer.git
cd fliqlo-timer
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
python main.py
```

### **Kiến Trúc**
- **Thiết kế module**: Tách biệt giao diện, logic, dữ liệu
- **Đa nền tảng**: Hỗ trợ Windows, macOS, Linux
- **Mã nguồn sạch**: Dễ đọc, dễ bảo trì
- **Dễ mở rộng**: Thêm tính năng mới dễ dàng

---

## 📜 Giấy Phép

MIT License - Tự do sử dụng, chỉnh sửa và chia sẻ.

---

## 🙏 Lời Cảm Ơn

- **Kỹ thuật Pomodoro**: Phương pháp quản lý thời gian của Francesco Cirillo
- **Thiết kế Fliqlo**: Lấy cảm hứng từ screensaver đồng hồ lật nổi tiếng  
- **Cộng đồng**: Người dùng Việt Nam và quốc tế yêu thích năng suất

---

**Chúc bạn học tập hiệu quả! 📚✨**
