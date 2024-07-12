import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Dữ liệu
X = np.array([1, 2, 3, 4, 5]).reshape(-1, 1)  # Giờ học
y = np.array([2, 3, 4, 5, 7])  # Điểm số

# Tạo mô hình và huấn luyện
model = LinearRegression()
model.fit(X, y)

# Dự đoán
y_pred = model.predict(X)

# Hệ số chặn và hệ số góc
print(f'Intercept: {model.intercept_}')
print(f'Slope: {model.coef_[0]}')

# Vẽ biểu đồ
plt.scatter(X, y, color='blue')  # Dữ liệu thực tế
plt.plot(X, y_pred, color='red')  # Đường hồi quy
plt.xlabel('Giờ học')
plt.ylabel('Điểm số')
plt.title('Hồi Quy Tuyến Tính')
plt.show()
