import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# 创建示例数据点
np.random.seed(0)
#100行2列
data = np.random.randn(100, 2) 

# 初始化 KMeans 模型，直接调用K_means算法代码
kmeans = KMeans(n_clusters=2, init='random', n_init=1)

# 迭代绘制结果
for i in range(5):  # 假设迭代 5 次
    kmeans.fit(data)

    # 绘制数据点和当前聚类中心
    plt.scatter(data[:, 0], data[:, 1], c=kmeans.labels_, cmap='viridis', alpha=0.5)
    plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], marker='x', c='red', s=100)
    plt.title(f"Iteration {i + 1}")
    plt.show()