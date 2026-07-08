# ĐỀ CƯƠNG CHI TIẾT ĐỒ ÁN TỐT NGHIỆP

# HỆ THỐNG DỰ BÁO THỜI TIẾT ỨNG DỤNG TRÍ TUỆ NHÂN TẠO BẰNG LSTM

## Chương 1. Tổng quan đề tài

### 1.1 Lý do chọn đề tài

Dự báo thời tiết đóng vai trò quan trọng trong nông nghiệp, giao thông,
du lịch và phòng chống thiên tai. Với sự phát triển của Trí tuệ nhân tạo
(AI), đặc biệt là Deep Learning, việc khai thác dữ liệu thời tiết lịch
sử để xây dựng mô hình dự báo ngày càng đạt độ chính xác cao hơn.

### 1.2 Mục tiêu

-   Thu thập dữ liệu thời tiết TP.HCM.
-   Tiền xử lý và phân tích dữ liệu.
-   Huấn luyện mô hình LSTM dự báo nhiệt độ.
-   Đánh giá mô hình bằng MAE, MSE, RMSE và R².
-   Xây dựng website hiển thị kết quả dự báo.

### 1.3 Phạm vi

-   Khu vực: TP.HCM
-   Dữ liệu: 01/01/2020 - 01/07/2026
-   Chu kỳ: 3 giờ/lần
-   Dự báo: Nhiệt độ.

------------------------------------------------------------------------

## Chương 2. Thu thập dữ liệu

Nguồn dữ liệu: - World Weather Online

Thu thập bằng: - Selenium - request_html

Thuộc tính: - Date - Time - Weather - Temp - Feels - Wind - Gust -
Rain - Humidity - Cloud - Pressure - Vis

Quy trình:

Website → Crawl → CSV → Kiểm tra → Tiền xử lý

------------------------------------------------------------------------

## Chương 3. Tiền xử lý và EDA

### Tiền xử lý

-   Xử lý Missing Value
-   Loại bỏ dữ liệu trùng
-   Chuyển đổi kiểu dữ liệu
-   Chuẩn hóa MinMaxScaler
-   Mã hóa Weather
-   Tạo Hour, Day, Month

### EDA

-   Thống kê mô tả
-   Histogram
-   Heatmap
-   Boxplot
-   Phân bố Weather
-   Nhiệt độ trung bình theo tháng
-   Lượng mưa trung bình theo tháng
-   Xu hướng nhiệt độ theo năm

------------------------------------------------------------------------

## Chương 4. Xây dựng mô hình LSTM

### Lý do lựa chọn

LSTM là mô hình Deep Learning phù hợp với dữ liệu chuỗi thời gian vì có
khả năng ghi nhớ thông tin trong quá khứ và học được các mối quan hệ dài
hạn.

### Chia dữ liệu

-   Train: 80%
-   Validation: 10%
-   Test: 10%

### Kiến trúc

Input

↓

LSTM(64)

↓

Dropout

↓

LSTM(32)

↓

Dense(1)

### Tham số

-   Epoch: 100
-   Batch Size: 32
-   Optimizer: Adam
-   Loss: Mean Squared Error

Quy trình: Chuẩn hóa → Tạo chuỗi thời gian → Train → Lưu model (.keras)

------------------------------------------------------------------------

## Chương 5. Đánh giá mô hình

Chỉ số: - MAE - MSE - RMSE - R² Score

Biểu đồ: - Loss - Actual vs Prediction - Sai số dự đoán - Dự đoán 100
mẫu cuối

------------------------------------------------------------------------

## Chương 6. Thiết kế hệ thống

Kiến trúc:

Crawler

↓

Preprocessing

↓

LSTM Model

↓

REST API

↓

Website React

↓

Người dùng

### Chức năng

-   Thu thập dữ liệu
-   Dự báo nhiệt độ
-   Dashboard
-   Biểu đồ
-   API

### Công nghệ

-   Python
-   TensorFlow/Keras
-   Pandas
-   NumPy
-   Matplotlib
-   Plotly
-   Selenium
-   Flask/FastAPI
-   ReactJS
-   PostgreSQL/MySQL

------------------------------------------------------------------------

## Chương 7. Kết luận và hướng phát triển

### Kết quả mong đợi

-   Mô hình LSTM dự báo chính xác.
-   Website hoạt động ổn định.
-   Dashboard trực quan.
-   API phục vụ dự báo.

### Hướng phát triển

-   Dự báo độ ẩm, lượng mưa và gió.
-   Dự báo nhiều mốc thời gian.
-   Tự động cập nhật dữ liệu.
-   Thử nghiệm GRU và Transformer.
-   Triển khai lên Cloud.
