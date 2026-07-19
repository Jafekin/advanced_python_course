import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


plt.rcParams['font.family'] = 'SimHei'  # 替换为你选择的字体
# 对基本配置进行设置，将中文字体设置为黑体，不包含中文负号，分辨率为 100，图像显示大小设置为 (5,3)。
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False
# plt.rcParams['figure.dpi'] = 100
# plt.rcParams['figure.figsize'] = (5,3)


data_all = pd.read_excel("grade_data.xlsx")
def classify(data:list):
    excellent = []
    good = []
    fair = []
    poor = []
    for grade in data:
        if 90 <= grade <= 100:
            excellent.append(grade)
        elif 80 <= grade < 90:
            good.append(grade)
        elif 60 <= grade < 80:
            fair.append(grade)
        elif 0 <= grade < 60:
            poor.append(grade)
    return excellent, good, fair, poor
data_p = data_all["程序设计基础"]
data_x = data_all["线性代数A"]

plt.hist(data_p)
plt.title("程序设计")
plt.show()
excellent1, good1, fair1, poor1 = classify(data_p)
excellent2, good2, fair2, poor2 = classify(data_x)
x = np.array(['excellent', 'good', 'fair', 'poor'])
y1 = np.array([len(excellent1), len(good1), len(fair1), len(poor1)])
y2 = np.array([len(excellent2), len(good2), len(fair2), len(poor2)])
x0 = np.arange(len(x))
x_p = x0 - 0.15
x_x = x0 + 0.15
plt.bar(x_p, y1,width=0.3)
plt.bar(x_x, y2,width=0.3)
plt.xticks(x0,x)
plt.title("程序设计与线性代数")
plt.ylabel("Scores")
plt.show()

fig, ax = plt.subplots()
flier_style = {
    'marker': 'D',       # 形状（菱形，使用大写字母D）
    'markerfacecolor': 'red',  # 填充色
    'markeredgecolor': 'black',  # 边缘色
    'markersize': 6      # 大小
}
VP = ax.boxplot([data_p,data_x],positions=[1,2],showfliers=True,flierprops=flier_style,)
plt.title("程序设计与线性代数")
plt.show()



