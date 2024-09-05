import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import talib
from backtesting import Backtest, Strategy

# Đọc dữ liệu
file_path = r'D:\startup\fx\merged_data_files.csv'
data = pd.read_csv(file_path)
# Đổi tên cột
data.columns = ['ngay', 'gio', 'Open', 'High', 'Low', 'Close', 'Volume']
# Kết hợp hai cột ngày và giờ
data['timestamp'] = pd.to_datetime(data['ngay'] + ' ' + data['gio'])
# Xóa hai cột ngay và gio ban đầu
data.drop(columns=['ngay', 'gio'], inplace=True)
# Đặt cột timestamp làm index
data.set_index('timestamp', inplace=True)
# Sắp xếp dữ liệu theo thời gian
data.sort_index(inplace=True)
data.reset_index(drop=False, inplace=True)
print(data.head())

# Tính toán các chỉ báo kỹ thuật nếu chưa có
if 'SMA' not in data.columns:
    data['SMA'] = talib.SMA(data['Close'], timeperiod=20)
if 'EMA' not in data.columns:
    data['EMA'] = talib.EMA(data['Close'], timeperiod=20) 
if 'RSI' not in data.columns:
    data['RSI'] = talib.RSI(data['Close'], timeperiod=14)
if 'Bollinger_High' not in data.columns:
    data['Bollinger_High'], data['Bollinger_Mid'], data['Bollinger_Low'] = talib.BBANDS(data['Close'], timeperiod=20)
if 'MACD' not in data.columns:
    data['MACD'], data['MACD_Signal'], data['MACD_Hist'] = talib.MACD(data['Close'], fastperiod=12, slowperiod=26, signalperiod=9)

    
data["Next_Close"] = data["Close"].shift(-1)
# # Xóa các hàng có giá trị NaN trong nhãn
data = data.dropna()
# # Lưu dữ liệu đã xử lý
data.to_csv('modified_data.csv', index=False)
# Khám phá dữ liệu
print(data.head())

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
features = ['SMA', 'EMA', 'RSI', 'Bollinger_High', 'Bollinger_Low', 'MACD']
X = data[features]
y = data['Next_Close']

# Loại bỏ hàng cuối cùng nếu vẫn còn NaN sau khi điền
X = X[:-1]
y = y[:-1]

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Xây dựng và huấn luyện mô hình với ít cây hơn để tăng tốc độ
model = RandomForestRegressor(n_estimators=50, max_depth=10, random_state=42)
model.fit(X_train, y_train)

# Định nghĩa chiến lược
class RandomForestStrategy(Strategy):
    def init(self):
        self.signal = self.I(lambda: self.data.Prediction)
        self.n_bars = 0  # Biến đếm số lượng nến đã qua kể từ khi lệnh được mở
        self.price_entry = None  # Biến lưu trữ giá tại thời điểm vào lệnh

    def next(self):
        # Đóng lệnh sau 5 cây nến
        if self.position:
            self.n_bars += 1
            if self.n_bars >= 5:
                self.position.close()
                self.n_bars = 0
                self.price_entry = None  # Reset giá vào lệnh khi đóng lệnh

        # Mở lệnh mới nếu không có lệnh nào đang mở
        if not self.position:
            if self.signal > self.data.Close:
                self.price_entry = self.data.Close[-1]  # Lưu giá đóng cửa hiện tại
                self.buy(sl=self.price_entry * 0.99, tp=self.price_entry * 1.01)  # Mua tại giá chỉ định
                self.n_bars = 0
            elif self.signal < self.data.Close:
                self.price_entry = self.data.Close[-1]  # Lưu giá đóng cửa hiện tại
                self.sell(sl=self.price_entry * 1.01, tp=self.price_entry * 0.99)  # Bán tại giá chỉ định
                self.n_bars = 0

# Thực hiện backtest
bt = Backtest(data, RandomForestStrategy, cash=10000, commission=.002)
stats = bt.run()
# print(stats)
bt.plot()