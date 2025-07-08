# Audio Files

This directory contains sound effects and background music for the Fliqlo Timer application.

## Required Files

The application expects the following audio files:

- `button_1.mp3` - Button click sound effect
- `whitenoise_1.mp3` - Background white noise for focus sessions
- `rang.mp3` - Session completion notification sound

## Audio Features

- **Button sounds**: Play when clicking buttons (Start, Pause, Reset, etc.)
- **Background music**: Plays continuously during timer sessions
  - Starts when pressing Start/Resume
  - Pauses when pressing Pause
  - Stops when pressing Reset
  - Automatically loops when finished

## Volume Control

- **Music Volume**: 0-100% (default 30%)
- **Button Volume**: 0-100% (default 70%)
- Can be adjusted within the application settings

## Audio Specifications

- **Format**: MP3 (recommended), WAV, or OGG
- **Quality**: 128 kbps or higher for MP3
- **Duration**: 
  - Button sounds: 0.1-0.5 seconds
  - Background music: 3-10 minutes (will loop)
  - Notification sounds: 1-3 seconds

## Customization

You can replace these files with your own audio:

1. Keep the same filenames
2. Use supported formats (MP3, WAV, OGG)
3. Ensure reasonable file sizes for performance

## License

Default audio files are included for demonstration purposes. For commercial use, please ensure you have proper licensing for any audio files you use.

## Định dạng được hỗ trợ:
- MP3 (đang dùng)
- WAV
- OGG

## Ghi chú:
- Ứng dụng sẽ hoạt động bình thường nếu thiếu file âm thanh
- Whitenoise giúp tập trung và che tiếng ồn xung quanh
