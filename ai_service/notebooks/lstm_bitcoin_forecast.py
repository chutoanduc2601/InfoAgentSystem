# =====================================================================
# KAGGLE NOTEBOOK TEMPLATE: LSTM Bitcoin Price Forecast
# =====================================================================
# Hướng dẫn trên Kaggle:
# 1. Tạo một Notebook mới trên Kaggle, bật GPU.
# 2. Upload file `btcusd_1-min_data.csv` lên Kaggle (Add Data -> Upload).
# 3. Copy toàn bộ đoạn code dưới đây vào Notebook và chạy.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam

# =====================================================================
# 1. LOAD DATA & TIỀN XỬ LÝ
# =====================================================================
DATASET_PATH = "/kaggle/input/bitcoin-historical-data/btcusd_1-min_data.csv"
if not os.path.exists(DATASET_PATH):
    DATASET_PATH = "btcusd_1-min_data.csv"

print(f"Loading Bitcoin dataset from: {DATASET_PATH}")
# Dùng chunks hoặc đọc trực tiếp (vì file lớn, có thể chọn sample hoặc lọc mốc thời gian gần đây)
# Khuyên nghị: Lọc dữ liệu từ năm 2023 đến nay để train nhanh hơn và chính xác với xu hướng hiện tại.
df = pd.read_csv(DATASET_PATH)

# Đổi tên các cột và xử lý Timestamp
if 'Timestamp' in df.columns:
    df['datetime'] = pd.to_datetime(df['Timestamp'], unit='s')
    df = df.dropna() # Xóa dòng NaN
    # Lọc lấy từ năm 2023 trở đi để tối ưu hóa thời gian train trên Kaggle
    df = df[df['datetime'] >= '2023-01-01'].reset_index(drop=True)
elif 'date' in df.columns:
    df['datetime'] = pd.to_datetime(df['date'])
    df = df.dropna().reset_index(drop=True)

df = df.sort_values('datetime').reset_index(drop=True)
print(f"Total rows after filtering: {len(df)}")

# Lấy cột giá đóng cửa 'Close' (hoặc 'Weighted_Price') để dự báo
target_col = 'Close' if 'Close' in df.columns else 'Weighted_Price'
print(f"Target column for forecasting: {target_col}")

# Downsample sang Daily hoặc Hourly để mô hình học dễ hơn và chạy nhanh hơn trên Kaggle (tránh tràn RAM do data 1-phút quá nhiều)
df.set_index('datetime', inplace=True)
# Resample thành dữ liệu trung bình mỗi 1 giờ (1H)
df_resampled = df[target_col].resample('1H').mean().interpolate(method='linear')
df_resampled = pd.DataFrame(df_resampled)

print(f"Data count after resample to 1-Hour: {len(df_resampled)}")

data = df_resampled.values
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# =====================================================================
# 2. TẠO CHUỖI THỜI GIAN
# =====================================================================
# Sử dụng 24 giờ trước để dự báo giá giờ tiếp theo
look_back = 24

def create_dataset(dataset, look_back=1):
    X, y = [], []
    for i in range(len(dataset) - look_back):
        X.append(dataset[i:(i + look_back), 0])
        y.append(dataset[i + look_back, 0])
    return np.array(X), np.array(y)

X, y = create_dataset(scaled_data, look_back)
# Reshape X sang dạng [samples, time steps, features] cho LSTM
X = np.reshape(X, (X.shape[0], X.shape[1], 1))
print(f"Shapes - X: {X.shape}, y: {y.shape}")

# Chia Train/Val/Test (80% - 10% - 10%)
n_samples = len(X)
train_end = int(n_samples * 0.8)
val_end = int(n_samples * 0.9)

X_train, y_train = X[:train_end], y[:train_end]
X_val, y_val = X[train_end:val_end], y[train_end:val_end]
X_test, y_test = X[val_end:], y[val_end:]

# =====================================================================
# 3. XÂY DỰNG MÔ HÌNH LSTM
# =====================================================================
model = Sequential([
    LSTM(64, return_sequences=True, input_shape=(X_train.shape[1], 1)),
    Dropout(0.2),
    LSTM(32, return_sequences=False),
    Dropout(0.2),
    Dense(1)
])

model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')
model.summary()

# Huấn luyện 50 epochs (đối với Bitcoin 50 epochs là đủ để hội tụ)
epochs = 50
batch_size = 64

history = model.fit(
    X_train, y_train,
    epochs=epochs,
    batch_size=batch_size,
    validation_data=(X_val, y_val),
    verbose=1
)

# =====================================================================
# 4. ĐÁNH GIÁ MÔ HÌNH
# =====================================================================
predictions = model.predict(X_test)

# Đưa về thang đo giá trị USD gốc
inv_predictions = scaler.inverse_transform(predictions)
inv_y_test = scaler.inverse_transform(y_test.reshape(-1, 1))

mae = mean_absolute_error(inv_y_test, inv_predictions)
mse = mean_squared_error(inv_y_test, inv_predictions)
rmse = np.sqrt(mse)
r2 = r2_score(inv_y_test, inv_predictions)

print("\n--- KẾT QUẢ ĐÁNH GIÁ MÔ HÌNH ---")
print(f"MAE: {mae:.2f} USD")
print(f"RMSE: {rmse:.2f} USD")
print(f"R² Score: {r2:.4f}")

# =====================================================================
# 5. VẼ BIỂU ĐỒ & LƯU MODEL
# =====================================================================
plt.figure(figsize=(12, 6))
plt.plot(inv_y_test[-100:], label='Giá BTC Thực tế', color='blue')
plt.plot(inv_predictions[-100:], label='Giá BTC Dự báo LSTM', color='red', linestyle='dashed')
plt.title('Dự báo Giá Bitcoin (100 mẫu giờ cuối)')
plt.ylabel('Giá USD')
plt.legend()
plt.savefig('bitcoin_prediction.png')
plt.close()

# Lưu model và scaler
model.save('bitcoin_lstm.keras')
import joblib
joblib.dump(scaler, 'bitcoin_scaler.pkl')
print("\nBitcoin Model & Scaler saved successfully.")
