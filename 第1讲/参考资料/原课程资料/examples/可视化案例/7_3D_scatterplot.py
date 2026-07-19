# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 11:30:15 2023

@author: 94526
"""


import numpy as np
import matplotlib.pyplot as plt
# 生成随机数
np.random.seed(19680801)
n = 100
rng = np.random.default_rng()
xs = rng.uniform(23, 32, n)
ys = rng.uniform(0, 100, n)
zs = rng.uniform(-50, -25, n)

# 获取画板和轴，绘制3维散点图
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
ax.scatter(xs, ys, zs)

ax.set(xticklabels=[],
       yticklabels=[],
       zticklabels=[])

plt.show()
