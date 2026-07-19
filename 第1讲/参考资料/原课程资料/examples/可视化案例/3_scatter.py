# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
# 设置随机数种子为3
np.random.seed(3)
# 生成正态分布的数据
x = 4 + np.random.normal(0, 2, 24)
y = 4 + np.random.normal(0, 2, len(x))
# 设置点的大小和颜色
sizes = np.random.uniform(15, 80, len(x))
colors = np.random.uniform(15, 80, len(x))
# 获取画板和轴
fig, ax = plt.subplots()
# 绘制散点图
ax.scatter(x, y, s=sizes, c=colors, vmin=0, vmax=100)

ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
       ylim=(0, 8), yticks=np.arange(1, 8))

plt.show()
