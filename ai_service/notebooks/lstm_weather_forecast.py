# =====================================================================
# KAGGLE NOTEBOOK TEMPLATE: LSTM Weather Forecast
# =====================================================================
# Hướng dẫn trên Kaggle:
# 1. Tạo một Notebook mới trên Kaggle, bật GPU (Settings -> Accelerator).
# 2. Upload file `hcm_weather_history.csv` lên Kaggle (Add Data -> Upload).
# 3. Copy toàn bộ đoạn code dưới đây vào Notebook và chạy.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam

# =====================================================================
# 1. LOAD DATA & TIỀN XỬ LÝ (Chương 2 & 3)
# =====================================================================
DATASET_PATH = "/kaggle/input/hcm-weather/hcm_weather_history.csv"
if not os.path.exists(DATASET_PATH):
    DATASET_PATH = "hcm_weather_history.csv"

print(f"Loading weather dataset from: {DATASET_PATH}")
df = pd.read_csv(DATASET_PATH)

# Chuyển đổi datetime và sắp xếp theo thời gian
df['datetime'] = pd.to_datetime(df['datetime'])
df = df.sort_values('datetime').reset_index(drop=True)

# Kiểm tra missing values
print("Missing values in dataset:")
print(df.isnull().sum())

# Điền giá trị thiếu nếu có (Interpolate)
df = df.interpolate(method='linear')

# Lấy các thuộc tính số làm features
features = ['temperature', 'humidity', 'rain', 'pressure', 'cloud', 'wind', 'gust']
data = df[features].values

# Chuẩn hóa dữ liệu về khoảng [0, 1] bằng MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# Chỉ số của temperature trong features (temperature ở vị trí index 0)
temp_idx = 0

# =====================================================================
# 2. TẠO CHUỖI THỜI GIAN (LOOKBACK WINDOW)
# =====================================================================
# Sử dụng 24 giờ trước (8 mẫu nếu chu kỳ 3 giờ, hoặc 24 mẫu nếu hourly) để dự báo nhiệt độ giờ tiếp theo
look_back = 24 

def create_dataset(dataset, look_back=1):
    X, y = [], []
    for i in range(len(dataset) - look_back):
        X.append(dataset[i:(i + look_back), :]) # Lấy tất cả features của look_back dòng trước
        y.append(dataset[i + look_back, temp_idx]) # Dự báo temperature dòng tiếp theo
    return np.array(X), np.array(y)

X, y = create_dataset(scaled_data, look_back)
print(f"Shapes - X: {X.shape}, y: {y.shape}")

# Chia dữ liệu theo tỷ lệ 80% Train - 10% Val - 10% Test (Chính xác theo Đề Cương)
n_samples = len(X)
train_end = int(n_samples * 0.8)
val_end = int(n_samples * 0.9)

X_train, y_train = X[:train_end], y[:train_end]
X_val, y_val = X[train_end:val_end], y[train_end:val_end]
X_test, y_test = X[val_end:], y[val_end:]

print(f"Train samples: {len(X_train)}")
print(f"Val samples: {len(X_val)}")
print(f"Test samples: {len(X_test)}")

# =====================================================================
# 3. EDA - TRỰC QUAN HÓA DỮ LIỆU (Chương 3)
# =====================================================================
print("\n--- Generating EDA Charts ---")
plt.figure(figsize=(10, 5))
plt.plot(df['datetime'][:1000], df['temperature'][:1000], label='Nhiệt độ (°C)', color='orange')
plt.title("Biểu đồ nhiệt độ theo thời gian (1000 mẫu đầu)")
plt.xlabel("Thời gian")
plt.ylabel("Nhiệt độ")
plt.legend()
plt.savefig("eda_temperature_trend.png")
plt.close()

# Heatmap tương quan giữa các biến
plt.figure(figsize=(8, 6))
sns.heatmap(df[features].corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Heatmap hệ số tương quan các thuộc tính thời tiết")
plt.tight_layout()
plt.savefig("eda_correlation_heatmap.png")
plt.close()

# =====================================================================
# 4. XÂY DỰNG MÔ HÌNH LSTM (Chương 4)
# =====================================================================
# Kiến trúc theo đề cương:
# Input -> LSTM(64) -> Dropout -> LSTM(32) -> Dense(1)
model = Sequential([
    LSTM(64, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])),
    Dropout(0.2),
    LSTM(32, return_sequences=False),
    Dropout(0.2),
    Dense(1)
])

model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')
model.summary()

# Train model 100 epochs, batch size 32
epochs = 100
batch_size = 32

history = model.fit(
    X_train, y_train,
    epochs=epochs,
    batch_size=batch_size,
    validation_data=(X_val, y_val),
    verbose=1
)

# =====================================================================
# 5. ĐÁNH GIÁ MÔ HÌNH (Chương 5)
# =====================================================================
# Dự đoán trên tập Test
predictions = model.predict(X_test)

# Đưa predictions và y_test về thang đo ban đầu (°C)
# Để làm điều này, ta tạo một ma trận ảo có kích thước tương tự để nghịch đảo transform
dummy_pred = np.zeros((len(predictions), len(features)))
dummy_pred[:, temp_idx] = predictions.flatten()
inv_predictions = scaler.inverse_transform(dummy_pred)[:, temp_idx]

dummy_actual = np.zeros((len(y_test), len(features)))
dummy_actual[:, temp_idx] = y_test
inv_y_test = scaler.inverse_transform(dummy_actual)[:, temp_idx]

# Tính toán các chỉ số
mae = mean_absolute_error(inv_y_test, inv_predictions)
mse = mean_squared_error(inv_y_test, inv_predictions)
rmse = np.sqrt(mse)
r2 = r2_score(inv_y_test, inv_predictions)

print("\n--- KẾT QUẢ ĐÁNH GIÁ MÔ HÌNH ---")
print(f"MAE (Mean Absolute Error): {mae:.4f} °C")
print(f"MSE (Mean Squared Error): {mse:.4f}")
print(f"RMSE (Root Mean Squared Error): {rmse:.4f} °C")
print(f"R² Score: {r2:.4f}")

# =====================================================================
# 6. VẼ BIỂU ĐỒ ĐÁNH GIÁ
# =====================================================================
# 1. Biểu đồ Loss
plt.figure(figsize=(10, 5))
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Val Loss')
plt.title('Biểu đồ Loss của Mô hình LSTM')
plt.xlabel('Epoch')
plt.ylabel('Loss (MSE)')
plt.legend()
plt.savefig('lstm_loss_curve.png')
plt.close()

# 2. Thực tế vs Dự báo (100 mẫu cuối)
plt.figure(figsize=(12, 6))
plt.plot(inv_y_test[-100:], label='Nhiệt độ Thực tế', marker='o', color='blue')
plt.plot(inv_predictions[-100:], label='Nhiệt độ Dự báo LSTM', marker='x', color='red', linestyle='dashed')
plt.title('So sánh Nhiệt độ Thực tế và Dự báo (100 mẫu cuối)')
plt.xlabel('Mẫu thời gian')
plt.ylabel('Nhiệt độ (°C)')
plt.legend()
plt.savefig('actual_vs_prediction.png')
plt.close()

# =====================================================================
# 7. LƯU MÔ HÌNH (.keras)
# =====================================================================
model_filename = 'hcm_weather_lstm.keras'
model.save(model_filename)
print(f"\nModel saved successfully as: {model_filename}")

# Lưu scaler để sau này backend dùng chuẩn hóa input khi inference
import joblib
scaler_filename = 'weather_scaler.pkl'
joblib.dump(scaler, scaler_filename)
print(f"Scaler saved successfully as: {scaler_filename}")

# Nén toàn bộ mô hình, scaler và các biểu đồ PNG thành file zip để tải về dễ dàng
import zipfile
import glob
zip_filename = 'weather_forecast_outputs.zip'
files_to_zip = glob.glob('*.png') + glob.glob('*.keras') + glob.glob('*.pkl')
with zipfile.ZipFile(zip_filename, 'w') as zipf:
    for file in files_to_zip:
        zipf.write(file)
print(f"Successfully zipped all outputs to: {zip_filename}")
