# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
# 生成数据
np.random.seed(10)
# 设置数据维度和每个维度的均值，标准差
D = np.random.normal((3, 5, 4), (1.25, 1.00, 1.25), (100, 3))

# 获取画板和轴
fig, ax = plt.subplots()
VP = ax.boxplot(D, positions=[2, 4, 6], widths=1.5, patch_artist=True,
                showmeans=False, showfliers=False,
# 各位置处的样式
                medianprops={"color": "white", "linewidth": 0.5},
                boxprops={"facecolor": "C0", "edgecolor": "white",
                          "linewidth": 0.5},
                whiskerprops={"color": "C0", "linewidth": 1.5},
                capprops={"color": "C0", "linewidth": 1.5})

ax.set(xlim=(0, 8), xticks=np.arange(2, 8, 2),
       ylim=(0, 8), yticks=np.arange(1, 8))

plt.show()
