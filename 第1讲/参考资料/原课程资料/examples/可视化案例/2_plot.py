# -*- coding: utf-8 -*-

import numpy as np

import matplotlib.pyplot as plt
# 生成数据，x为0到10内均匀分布的100个数据点
x = np.linspace(0, 10, 100)
# 生成对应的y值
y = 4 + 2 * np.sin(2 * x)

# 获取画板和轴
fig, ax = plt.subplots()

ax.plot(x, y, linewidth=2.0)

# 设置轴参数
ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
       ylim=(0, 8), yticks=np.arange(1, 8))

plt.show()
