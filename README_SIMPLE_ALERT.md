# Simple Alert System - OpenPilot Simplified

🚗 **Hệ thống cảnh báo đơn giản dựa trên OpenPilot - Chỉ cảnh báo, không tự động lái**

## ✨ Tính năng

- ⚠️ **Cảnh báo lệch làn đường** (Left/Right Lane Departure)
- 👁️ **Phát hiện chuyển động** (Motion Detection)
- 🔊 **Cảnh báo âm thanh** (Audio Alerts)
- 📱 **Kết nối camera điện thoại** (Phone Camera Support)
- 📸 **Chụp ảnh màn hình** (Screenshot Capability)

## 🚀 Cách chạy (1 lệnh duy nhất)

### Trên Windows:
```bash
start_alert.bat
```

### Hoặc chạy trực tiếp Python:
```bash
python start_alert_system.py
```

## 📱 Kết nối Camera Điện thoại

### Bước 1: Cài đặt app trên điện thoại
- **Android**: IP Webcam (by Pavel Khlebovich)
- **iOS**: EpocCam hoặc app IP camera tương tự

### Bước 2: Kết nối mạng
- Kết nối điện thoại và máy tính cùng WiFi
- Khởi động app IP camera trên điện thoại
- Ghi nhớ địa chỉ IP (ví dụ: 192.168.1.100:8080)

### Bước 3: Sửa source camera
Mở file `simple_alert_system.py` và sửa dòng:
```python
# Thay đổi từ:
source=0

# Thành:
source='http://YOUR_PHONE_IP:8080/video'
```

### Bước 4: Chạy lại hệ thống
```bash
python start_alert_system.py
```

## 🎮 Điều khiển

- **q**: Thoát hệ thống
- **s**: Chụp ảnh màn hình
- **ESC**: Thoát (nếu có)

## 📋 Yêu cầu hệ thống

- Python 3.7+
- Camera (webcam hoặc điện thoại)
- Windows/Linux/MacOS

## 🔧 Cài đặt tự động

Script sẽ tự động cài đặt các thư viện cần thiết:
- opencv-python
- numpy
- pyzmq
- pycapnp
- tqdm
- zstandard

## ⚠️ Lưu ý quan trọng

- **KHÔNG CÓ TÍNH NĂNG TỰ ĐỘNG LÁI XE**
- Chỉ cung cấp cảnh báo và giám sát
- Sử dụng cho mục đích học tập và nghiên cứu
- Không thay thế cho hệ thống an toàn của xe

## 🐛 Xử lý sự cố

### Camera không hoạt động:
1. Kiểm tra kết nối camera
2. Thử đổi source camera (0, 1, 2...)
3. Kiểm tra quyền truy cập camera

### Lỗi import:
1. Chạy: `pip install -r requirements.txt`
2. Hoặc chạy lại `start_alert_system.py` để tự động cài đặt

### Điện thoại không kết nối được:
1. Kiểm tra cùng WiFi network
2. Kiểm tra firewall/antivirus
3. Thử đổi port trong app IP camera

## 📞 Hỗ trợ

Nếu gặp vấn đề, hãy kiểm tra:
1. Logs trong terminal
2. Kết nối camera
3. Phiên bản Python
4. Quyền truy cập camera

---

**🎯 Mục tiêu**: Tạo hệ thống cảnh báo đơn giản, dễ sử dụng, chỉ cần 1 lệnh để chạy!
