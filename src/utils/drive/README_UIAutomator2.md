# UI Automator 2 Migration Guide

## Overview

Đã chuyển đổi từ Appium sang UI Automator 2 cho các thao tác trên Android. UI Automator 2 là một framework testing mạnh mẽ của Google, hoạt động trực tiếp trên device mà không cần server.

## Các file đã chuyển đổi

### 1. UtilActionsClick.py

- **Click operations**: Click vào elements theo các selector khác nhau
- **Coordinate click**: Click vào tọa độ cụ thể
- **Long click & Double click**: Click giữ và click đôi
- **Drag & Drop**: Kéo thả elements

### 2. UtilActionsGetElements.py

- **Find elements**: Tìm elements theo các selector
- **Multiple elements**: Lấy danh sách elements
- **Wait for elements**: Chờ element xuất hiện
- **Image matching**: Tìm element bằng hình ảnh
- **File operations**: Push/pull files

### 3. UtilActionsRedirect.py

- **Navigation**: Back, Home, Recent apps
- **App management**: Mở/đóng ứng dụng
- **Intent operations**: Mở link, deep link
- **Screen operations**: Lock/unlock screen

### 4. UtilActionsScroll.py

- **Vertical/Horizontal scroll**: Scroll theo các hướng
- **Scroll to element**: Scroll đến khi tìm thấy element
- **Fling gestures**: Vuốt nhanh
- **Scroll in view**: Scroll trong container cụ thể

## Cách sử dụng

### 1. Khởi tạo device

```python
import uiautomator2 as u2

# Kết nối qua USB
device = u2.connect()  # hoặc u2.connect("serial_number")

# Kết nối qua WiFi
device = u2.connect("192.168.1.100")
```

### 2. Các selector phổ biến

```python
# Theo resource ID
selector = 'resourceId("com.instagram.android:id/button")'

# Theo text
selector = 'text("Login")'
selector = 'textContains("Log")'  # Chứa text

# Theo content description
selector = 'description("Home button")'
selector = 'descriptionContains("Home")'

# Theo class name
selector = 'className("android.widget.Button")'

# Kết hợp các điều kiện
selector = 'className("android.widget.Button").textContains("Login")'
```

### 3. Ví dụ sử dụng

```python
from utils.drive import UtilActionsClick, UtilActionsGetElements

# Click element
UtilActionsClick.click_on_element_by_text(device, "Login")

# Click bằng resource ID
UtilActionsClick.click_on_element_by_resource_id(device, "com.app:id/button")

# Get element
element = UtilActionsGetElements.get_element_by_text(device, "Settings")
if element:
    print("Element found!")

# Scroll để tìm element
found = UtilActionsScroll.scroll_vertical_until_find_element_by_selector(
    device,
    'text("Load more")',
    max_scroll_find=10
)
```

### 4. Backward compatibility

Các function cũ vẫn được giữ lại với wrapper:

```python
# Vẫn có thể dùng xpath như cũ
UtilActionsClick.click_on_element_wait_by_xpath(
    device,
    '//android.widget.Button[@text="Login"]'
)

# XPath sẽ được tự động chuyển thành UIAutomator2 selector
```

## Ưu điểm của UI Automator 2

1. **Không cần server**: Trực tiếp chạy trên device
2. **Nhanh hơn**: Giảm latency so với Appium
3. **Stability**: Ít lỗi connection hơn
4. **Native support**: Hoạt động tốt với Android native apps
5. **WiFi/USB**: Hỗ trợ cả 2 cách kết nối
6. **Debug dễ dàng**: Có thể xem device info real-time

## Cài đặt

```bash
pip install uiautomator2

# Cài đặt trên device (chỉ cần làm 1 lần)
python -m uiautomator2 init
```

## Khác biệt chính so với Appium

| Feature    | Appium            | UI Automator 2   |
| ---------- | ----------------- | ---------------- |
| Server     | Cần Appium Server | Không cần server |
| Connection | HTTP/JSON         | Direct ADB/WiFi  |
| Speed      | Chậm hơn          | Nhanh hơn        |
| Setup      | Phức tạp          | Đơn giản         |
| XPath      | Full support      | Partial support  |
| iOS        | Hỗ trợ            | Không hỗ trợ     |

## Tips & Best Practices

### 1. Sử dụng selector thay vì XPath

```python
# Thay vì dùng XPath phức tạp
xpath = '//android.widget.Button[@resource-id="com.app:id/button" and @text="Login"]'

# Dùng selector đơn giản hơn
selector = 'resourceId("com.app:id/button").text("Login")'
```

### 2. Wait cho element

```python
# Thay vì time.sleep()
time.sleep(5)

# Dùng wait
element = device(text="Login").wait(timeout=5000)  # 5 seconds
```

### 3. Error handling

```python
try:
    element = device(text="Login")
    if element.exists:
        element.click()
except Exception as e:
    print(f"Error: {e}")
```

### 4. Chain operations

```python
# Chain multiple operations
device(text="Settings").click().wait(timeout=3000)
```

## Debug

### 1. Xem XML hierarchy

```python
# Dump XML to file
device.dump_hierarchy("ui_dump.xml")

# Hoặc xem trực tiếp
print(device.dump_hierarchy())
```

### 2. Screenshot

```python
# Chụp màn hình
screenshot = device.screenshot()
screenshot.save("screen.png")

# Chụp và lưu trực tiếp
device.screenshot("screen.png")
```

### 3. Device info

```python
# Xem thông tin device
print(device.info)

# Xem window size
print(device.window_size())

# Xem current app
print(device.app_current())
```

## Troubleshooting

### 1. Device không kết nối

```bash
# Kiểm tra device
adb devices

# Restart ADB
adb kill-server
adb start-server

# Kiểm tra WiFi connection
ping <device_ip>
```

### 2. Element không tìm thấy

```python
# Kiểm tra selector
device(text="Login").exists  # True/False

# Xem tất cả elements với class
device(className="android.widget.Button").all()

# Dùng inspector
python -m uiautomator2 inspector
```

### 3. Permission issues

```bash
# Grant permissions
adb shell pm grant <package> android.permission.WRITE_EXTERNAL_STORAGE

# Check permissions
adb shell dumpsys package <package> | grep permission
```

## Performance Optimization

1. **Dùng device ID thay vì IP** cho USB connection
2. **Cache selectors** khi dùng nhiều lần
3. **Avoid excessive screenshots**
4. **Use wait() thay vì time.sleep()**
5. **Batch operations** khi possible

## Migration Checklist

- [ ] Cài đặt uiautomator2
- [ ] Init device với `uiautomator2 init`
- [ ] Thay đổi import statements
- [ ] Update device initialization
- [ ] Test các functions chính
- [ ] Update error handling
- [ ] Add performance monitoring
