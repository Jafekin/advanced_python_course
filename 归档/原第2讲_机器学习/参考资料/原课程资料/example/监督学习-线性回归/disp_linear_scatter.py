import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 准备数据
X = np.array([5.1, 8.2, 11.5, 13.9, 15.1, 16.2, 19.6, 23.3]).reshape(-1, 1)
Y = np.array([2.14, 4.62, 8.24, 11.24, 13.99, 16.33, 19.23, 28.74]).reshape(-1, 1)

# 2. 划分训练集和测试集
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.3, random_state=42
)

# 3. 初始化并训练线性回归模型（仅用训练集）
regressor = LinearRegression()
regressor.fit(X_train, Y_train)

# 4. 用测试集预测
Y_test_pred = regressor.predict(X_test)
print(Y_test)
print(Y_test_pred)

# 5. 可视化：训练集拟合效果 + 测试集预测效果
plt.figure(figsize=(10, 6))

# 绘制训练集
plt.scatter(X_train, Y_train, color='red', label='训练集样本')
plt.plot(X_train, regressor.predict(X_train), color='blue', label='训练集')

# 绘制测试集
plt.scatter(X_test, Y_test, color='green', label='测试集真实值')
plt.plot(X_test, Y_test_pred, color='orange', linestyle='--', label='测试集')

plt.title('训练集vs测试集')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.show()