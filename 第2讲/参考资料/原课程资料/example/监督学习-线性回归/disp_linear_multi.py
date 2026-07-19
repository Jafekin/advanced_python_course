import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# 输入特征和输出目标数据
temperatures = np.array([5.1, 8.2, 11.5, 13.9, 15.1, 16.2, 19.6, 23.3])
winds = np.array([4.5, 5.8, 4.0, 6.3, 4.0, 7.2, 6.3, 8.5])
fire_areas = np.array([2.14, 4.62, 8.24, 11.24, 13.99, 16.33, 19.23, 28.74])

# 创建一个三维图形
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 将输入特征组合成矩阵
X = np.column_stack((temperatures, winds))

# 线性回归模型
model = LinearRegression()
model.fit(X, fire_areas)

# 生成平面上的点
temperatures_mesh, winds_mesh = np.meshgrid(np.linspace(temperatures.min(), temperatures.max(), 20),
                                            np.linspace(winds.min(), winds.max(), 20))
X_grid = np.column_stack((temperatures_mesh.ravel(), winds_mesh.ravel()))

# 预测平面上的点的输出值
fire_areas_pred = model.predict(X_grid)
fire_areas_pred = fire_areas_pred.reshape(temperatures_mesh.shape)

# 绘制散点图
ax.scatter(temperatures, winds, fire_areas, c='r', marker='o', label='Actual Data')

# 绘制拟合平面
ax.plot_surface(temperatures_mesh, winds_mesh, fire_areas_pred, alpha=0.3, cmap='viridis')

# 设置坐标轴标签
ax.set_xlabel('Temperature')
ax.set_ylabel('Wind')
ax.set_zlabel('Size')

plt.legend()
plt.show()