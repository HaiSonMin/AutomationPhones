oke giờ hãy đưa workers\remote-pc\v2\agent\sfu_agent vào trong tính năng của tools\phones\src\features\remote

Hiện tại sfu_agent chính là 1 module. Tôi muốn di chuyển qua phía tools\phones\src\features\remote để có thể tích hợp vào trong ứng dụng.

- YÊU CẦU PHÍA PYTHON:

* Hiện tại workers\remote-pc\v2\agent\sfu_agent chưa có tính năng lưu token và thông tin của user đăng nhập, nhưng tools\phones\src\bridge\auth đã có tính năng lưu token và thông tin của user đăng nhập IUser.
* Hãy chỉnh sửa lại workers\remote-pc\v2\sfu để security token và thông tin của user đăng nhập IUser dựa theo token đã lưu trong tools\phones
* tools\phones\.env tôi đã chỉnh để phù hợp với hệ thông.
  _\*\* PC_ID: Bạn có thể lấy machineGUID từ hệ thống => Không cần phải thông qua .env
  _\*\* PC_NAME: Tên máy tính đang chạy => Không cần phải thông qua .env
