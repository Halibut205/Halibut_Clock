# Data Directory

This directory contains application data files that are automatically created and managed by the Study Timer.

## Files

### `tasks_data.json`
- **Description**: JSON database containing all tasks
- **Auto-created**: When the application runs for the first time
- **Structure**:
  ```json
  {
    "tasks": [...],
    "completed_tasks": [...],
    "last_updated": "ISO datetime"
  }
  ```

### `app_settings.json`
- **Description**: User preferences and application settings
- **Auto-created**: When settings are first modified
- **Contains**: Volume settings, window preferences, session configurations

### `daily_stats.json`
- **Description**: Daily study statistics and progress tracking
- **Auto-created**: When statistics are first recorded
- **Contains**: Study time, break time, session counts, task completion data

## Data Management

- **Automatic Creation**: All files are created automatically when needed
- **Backup**: Consider backing up this directory to preserve your data
- **Reset**: Delete files to reset specific data (app will recreate them)
- **Format**: All files use JSON format for easy reading and editing

## Privacy

- All data is stored locally on your computer
- No data is sent to external servers
- Files contain only usage statistics and preferences

## Troubleshooting

- **Corrupted data**: Delete the problematic JSON file and restart the app
- **Missing files**: Normal - they will be recreated automatically
- **Large files**: Statistics data grows over time but remains manageable

## Manual Editing

While possible, manual editing is not recommended unless you're familiar with JSON format. Always backup files before editing.

Để backup tasks:
1. Copy file `tasks_data.json` 
2. Lưu với tên khác (VD: `tasks_backup_20250105.json`)

Để restore:
1. Copy file backup thành `tasks_data.json`
2. Restart ứng dụng
