import numpy as np
import matplotlib.pyplot as plt

# 手动实现K_means算法的代码
def k_means(X, k, max_iters=100):
    # 获取样本总数与维度
    n_samples, n_features = X.shape
    # 随机选择k个样本作为初始质心
    centroids = X[np.random.choice(n_samples, k, replace=False)]
    labels = np.zeros(n_samples)
    for _ in range(max_iters):
        # 计算每个样本到每个质心的欧氏距离，为样本分配新的簇标签
        distances = np.linalg.norm(X[:, np.newaxis] - centroids, axis=2)
        new_labels = np.argmin(distances, axis=1)
        # 判断算法是否收敛，若结果不变，终止运行
        if np.array_equal(new_labels, labels):
            break
        labels = new_labels
        for i in range(k):
            centroids[i] = np.mean(X[labels == i], axis=0)
    return labels, centroids



# 生成测试数据
np.random.seed(42)
circle1 = np.random.normal(loc=[1, 1], scale=0.5, size=(100, 2))
circle2 = np.random.normal(loc=[2, 2], scale=0.5, size=(100, 2))
X = np.vstack((circle1, circle2))

# 执行K-means算法
k = 2
labels, centroids = k_means(X, k)

# 绘制散点图
plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis')
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', marker='X', s=100, label='Centroids')
plt.title('K-means Clustering')
plt.legend()
plt.show()