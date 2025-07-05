# Data Directory

Thư mục này chứa các file dữ liệu của ứng dụng.

## Files

### `tasks_data.json`
- **Mô tả**: Database JSON chứa tất cả tasks
- **Tự động tạo**: Khi chạy ứng dụng lần đầu
- **Cấu trúc**:
  ```json
  {
    "tasks": [...],
    "completed_tasks": [...],
    "last_updated": "ISO datetime"
  }
  ```

## Backup

Để backup tasks:
1. Copy file `tasks_data.json` 
2. Lưu với tên khác (VD: `tasks_backup_20250105.json`)

Để restore:
1. Copy file backup thành `tasks_data.json`
2. Restart ứng dụng
