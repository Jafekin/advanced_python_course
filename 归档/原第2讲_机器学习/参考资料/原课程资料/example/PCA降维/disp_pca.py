import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# 生成二维数据
np.random.seed(42)
mean = [0, 0]
cov = [[1, 0.8], [0.8, 1]]
X = np.random.multivariate_normal(mean, cov, 100)

# 绘制原始数据散点图
plt.scatter(X[:, 0], X[:, 1], alpha=0.6)
plt.title('Original Data')
plt.xlabel('Feature1')
plt.ylabel('Feature2')
plt.show()

# 使用PCA降维到一维
pca = PCA(n_components=1)
X_pca = pca.fit_transform(X)

# 将降维后的数据恢复到原始维度
X_reconstructed = pca.inverse_transform(X_pca)

# 绘制降维后数据恢复的效果
plt.scatter(X_reconstructed[:, 0], X_reconstructed[:, 1], alpha=0.6)
plt.title('Processed Data')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.show()