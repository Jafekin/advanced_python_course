import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 创建示例数据
cons = 100000
months = np.arange(1, 13)
prices = np.random.randint(80, 100, size=len(months))
monthly_sales = [int(cons / price * np.random.uniform(0.9, 1.1)) for price in prices]
profit = [s * p for s, p in zip(monthly_sales, prices)]

df = pd.DataFrame({'months': months, 'prices': prices, 'monthly_sales': monthly_sales})

# -------- 第一张图：饼状图（月销售占比） --------
plt.figure(figsize=(8, 8))
plt.pie(monthly_sales, labels=months, autopct='%.1f%%', shadow=False)
plt.title('Monthly Sales Distribution')
plt.show()

# -------- 第二张图：散点图（月销售额与产品价格关系） --------
plt.figure(figsize=(10, 6))
plt.scatter(prices, monthly_sales, c='r', marker='o', label='Months')
plt.xlabel('Price')
plt.ylabel('Monthly Sales')
plt.title('Monthly Sales vs Price')
plt.legend()
plt.show()

# -------- 第三张图：条形图（每月销售额） --------
plt.figure(figsize=(10, 6))
plt.bar(months, monthly_sales, color='g')
plt.xlabel('Month')
plt.ylabel('Monthly Sales')
plt.title('Monthly Sales')
plt.ylim(500, 1500)
plt.show()

# -------- 第四张图：折线图（月销售额和价格趋势，双轴） --------
plt.figure(figsize=(10, 6))
ax1 = plt.gca()  # 获取当前轴
ax2 = ax1.twinx()  # 创建第二个 y 轴，共享 x 轴

ax1.set_ylim(60, 120)
ax2.set_ylim(800, 1400)
ax1.plot(months, prices, label='Prices', color='b')
ax2.plot(months, monthly_sales, label='Monthly Sales', color='g')

ax1.set_xlabel('Month')
ax1.set_ylabel('Prices', color='b')
ax2.set_ylabel('Monthly Sales', color='g')

ax1.tick_params(axis='y', labelcolor='b')
ax2.tick_params(axis='y', labelcolor='g')

plt.title('Sales and Monthly Sales Trend')
plt.show()