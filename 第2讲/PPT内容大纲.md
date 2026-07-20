# 第二讲：数据高阶可视化与 AI 辅助表达

## PPT 内容大纲（约 44 张 Slides）

---

### Slide 1｜封面

**标题**：Python 进阶 · 第 2 讲
**副标题**：数据高阶可视化 × AI 辅助表达
**教师**：孙青 / 欧阳元新 · 计算机学院
**平台**：CloudStudio + CodeBuddy

---

### Slide 2｜本讲全景导航

**从"数据"到"视觉表达"：**

| 板块 | 内容 | AI 协作 |
|------|------|---------|
| Part 1 | Matplotlib 进阶与图表决策 | 图表类型推荐 |
| Part 2 | Seaborn 高阶可视化 | 方案对比建议 |
| Part 3 | 科研论文图表 | 发表级排版指导 |
| Part 4 | AI 辅助可视化表达 | 三轮迭代优化 |

> AI 角色定位：**设计顾问**——图表方案生成、视觉审查、结论修正

---

### Slide 3｜承上启下：从数据到表达

```
第1讲：数据处理（加载→清洗→统计）→ 得到"数字结论"
第2讲：数据可视化（本讲）        → 把数字转化为"视觉证据"
第3讲：工程化                    → 把一次性脚本变成可复用系统
```

**本讲核心问题**：如何把数据分析的结果转化为**可信的、发表级的**视觉表达？

---

### Slide 4｜本讲数据集：NASA 全球气温异常

**数据来源**：NASA GISS Surface Temperature Analysis (GISTEMP v4)

- `global_temperature.csv`：1880-2024 年全球月度/年度气温距平（相对于 1951-1980 基线）
- 约 1740 行 × 4 列（Source, Year/Month, Mean anomaly）
- 两个数据源：GISTEMP（NASA）、GCAG（NOAA）

**为什么选这个数据？**
- 真实科学数据，不是玩具
- 天然适合：折线图、误差棒、热力图、置信区间、统计标注
- 全球变暖是学生都了解的话题，降低认知负担

---

## Part 1：Matplotlib 进阶与图表决策（~10 张）

### Slide 5｜图表决策树：什么数据用什么图

| 分析目标 | 推荐图表 | 方法 |
|---------|---------|------|
| 看分布 | 直方图 / KDE | `plt.hist()` / `sns.kdeplot()` |
| 比类别 | 柱状图 | `plt.bar()` |
| 看关系 | 散点图 | `plt.scatter()` |
| 看趋势 | 折线图 | `plt.plot()` |
| 比多组分布 | 箱线图 / 小提琴图 | `plt.boxplot()` / `sns.violinplot()` |
| 看相关 | 热力图 | `sns.heatmap()` |
| 看联合分布 | Jointplot | `sns.jointplot()` |

**决策口诀**：一变量看形态，两变量看关系，多类别看分布。

---

### Slide 6｜折线图进阶：全球气温趋势

```python
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('global_temperature.csv')
annual = df[df['Source'] == 'GISTEMP'].groupby('Year')['Mean'].mean()

fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(annual.index, annual.values, color='#E74C3C', linewidth=1.5)
ax.axhline(0, color='gray', linestyle='--', alpha=0.5)
ax.fill_between(annual.index, annual.values, 0,
                where=(annual.values > 0), color='#E74C3C', alpha=0.3)
ax.fill_between(annual.index, annual.values, 0,
                where=(annual.values < 0), color='#3498DB', alpha=0.3)
ax.set_title('全球年均气温距平（1880-2024）')
ax.set_xlabel('年份')
ax.set_ylabel('温度距平 (°C)')
```

---

### Slide 7｜柱状图进阶：分组与堆叠

```python
# 按年代分组统计
decades = annual.groupby(annual.index // 10 * 10).mean()

fig, ax = plt.subplots(figsize=(12, 5))
colors = ['#3498DB' if v < 0 else '#E74C3C' for v in decades.values]
ax.bar(decades.index.astype(str), decades.values, color=colors, width=0.7)
ax.axhline(0, color='black', linewidth=0.8)
ax.set_title('各年代平均气温距平')

# 添加数值标签
for i, v in enumerate(decades.values):
    ax.text(i, v + 0.02, f'{v:.2f}', ha='center', fontsize=9)
```

---

### Slide 8｜直方图与 KDE：分布可视化

```python
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# 直方图
axes[0].hist(annual.values, bins=25, color='steelblue', edgecolor='white')
axes[0].axvline(annual.mean(), color='red', linestyle='--', label=f'均值={annual.mean():.2f}')
axes[0].set_title('气温距平分布')
axes[0].legend()

# KDE（核密度估计）
import seaborn as sns
sns.kdeplot(annual.values, ax=axes[1], fill=True, color='coral')
axes[1].set_title('气温距平核密度估计')
```

---

### Slide 9｜多子图布局：一次呈现多个视角

```python
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

axes[0,0].plot(...)       # 趋势折线
axes[0,1].bar(...)        # 年代对比柱状
axes[1,0].hist(...)       # 分布直方
axes[1,1].boxplot(...)    # 季节箱线

plt.tight_layout()
plt.savefig('overview.png', dpi=300, bbox_inches='tight')
```

**关键参数**：
- `figsize`：控制整体大小
- `tight_layout()`：自动调间距
- `savefig(dpi=300)`：发表级分辨率

---

### Slide 10｜图表美化系统化

```python
# 全局样式设置（放在代码开头）
plt.rcParams.update({
    'font.sans-serif': ['Arial Unicode MS', 'SimHei'],  # 中文支持
    'axes.unicode_minus': False,
    'figure.dpi': 100,
    'savefig.dpi': 300,
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.labelsize': 11,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.figsize': (10, 6),
})
```

**发表级图表三要素**：高分辨率(300dpi) + 清晰标注 + 一致字号

---

### Slide 11｜AI 协作：让 AI 推荐图表类型

**课堂练习**：

```
我有一个全球气温距平数据集，包含 1880-2024 年的月度数据，
有两个数据源（GISTEMP 和 GCAG）。

我想展示以下分析结果：
1. 长期变暖趋势
2. 近30年变暖加速
3. 各月份的变暖差异
4. 两个数据源的一致性

请为每个分析目标推荐最合适的图表类型，并说明原因。
```

> AI 角色 = 设计顾问：先推荐方案，再由你决定

---

## Part 2：Seaborn 高阶可视化（~10 张）

### Slide 12｜Seaborn vs Matplotlib

| | Matplotlib | Seaborn |
|---|---|---|
| 定位 | 底层绑图引擎 | 统计可视化高层封装 |
| 语法 | 面向对象，精细控制 | 函数式，一行出图 |
| 默认样式 | 朴素 | 现代美观 |
| 数据格式 | 数组/列表 | 推荐长格式 DataFrame |
| 适合场景 | 高度自定义 | 快速探索+统计图 |

**原则**：Seaborn 快速出图 → Matplotlib 精细调整

---

### Slide 13｜热力图 heatmap：相关性可视化

```python
import seaborn as sns

# 构造月份×年代 的气温距平矩阵
pivot = monthly_df.pivot_table(values='Mean', index='Month', columns='Decade')

fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(pivot, cmap='RdBu_r', center=0, annot=True, fmt='.2f',
            linewidths=0.5, ax=ax)
ax.set_title('各月份×各年代 气温距平热力图')
ax.set_xlabel('年代')
ax.set_ylabel('月份')
```

**应用场景**：相关系数矩阵、时间×类别的数值密度、混淆矩阵

---

### Slide 14｜小提琴图 violinplot：分布 + 密度

```python
fig, ax = plt.subplots(figsize=(12, 5))
sns.violinplot(data=seasonal_df, x='Season', y='Mean',
               palette='Set2', inner='quartile', ax=ax)
ax.set_title('各季节气温距平分布')
ax.axhline(0, color='gray', linestyle='--', alpha=0.5)
```

**vs 箱线图**：
- 箱线图只显示 5 个统计量
- 小提琴图额外展示数据密度分布形态（双峰？偏态？）

---

### Slide 15｜Pairplot：多变量关系全景

```python
# 对多个数值列做两两关系全景图
cols = ['Annual_Mean', 'DJF', 'MAM', 'JJA', 'SON']
sns.pairplot(df[cols], diag_kind='kde', corner=True,
             plot_kws={'alpha': 0.5, 's': 20})
```

**适用场景**：
- 变量不多（4-6个）时的快速探索
- 一眼看出哪些变量强相关、哪些独立

---

### Slide 16｜Jointplot：联合分布 + 边际

```python
sns.jointplot(data=df, x='Year', y='Mean', kind='hex',
              marginal_kws={'bins': 30})
```

**kind 参数**：
- `scatter`：散点 + 边际直方图
- `kde`：二维核密度
- `hex`：六边形分箱（数据量大时高效）
- `reg`：散点 + 回归线

---

### Slide 17｜FacetGrid 分面图：按类别拆分

```python
g = sns.FacetGrid(monthly_long, col='Season', col_wrap=2,
                  height=4, aspect=1.5)
g.map_dataframe(sns.lineplot, x='Year', y='Mean')
g.set_titles('{col_name}')
g.set_axis_labels('年份', '气温距平 (°C)')
```

**适用场景**：同一图形按类别拆分对比（如四个季节各自的趋势）

---

### Slide 18｜AI 协作：Seaborn 方案对比

**课堂练习**：

```
我想对比全球气温数据中四个季节（春夏秋冬）的变暖趋势差异。
请给出 3 种不同的 Seaborn 可视化方案，说明各自的优缺点。
数据是长格式：Year / Season / Mean_Anomaly
```

> 让 AI 给出多方案 → 你选择最合适的 → AI 生成代码

---

## Part 3：科研论文图表（~10 张）

### Slide 19｜科研图表的标准

| 要素 | 要求 | 常见错误 |
|------|------|---------|
| 分辨率 | 300 dpi（Nature/Science 要求） | 默认 100 dpi 太模糊 |
| 字号 | 正文 8-10pt，标题 10-12pt | 字太小看不清 |
| 线宽 | 0.5-1.5pt | 太粗覆盖数据 |
| 配色 | 色盲友好 + 可区分 | 红绿配色对色盲不友好 |
| 图例 | 不遮挡数据 | 图例盖住关键区域 |
| 白色背景 | 大多数期刊要求白底 | 带灰色网格 |

---

### Slide 20｜误差棒图 errorbar

```python
# 每年代的均值±标准差
decade_stats = annual.groupby(annual.index // 10 * 10).agg(['mean', 'std'])

fig, ax = plt.subplots(figsize=(10, 5))
ax.errorbar(decade_stats.index, decade_stats['mean'], yerr=decade_stats['std'],
            fmt='o-', capsize=4, capthick=1.5, color='#2C3E50', 
            ecolor='#E74C3C', markersize=6)
ax.axhline(0, color='gray', linestyle='--')
ax.set_title('各年代气温距平（均值±标准差）')
ax.set_xlabel('年代')
ax.set_ylabel('温度距平 (°C)')
```

**应用**：实验重复测量的不确定性展示（毕业论文必用）

---

### Slide 21｜置信区间可视化：fill_between

```python
# 计算滑动窗口的均值和95%置信区间
window = 10
rolling_mean = annual.rolling(window).mean()
rolling_std = annual.rolling(window).std()
ci_upper = rolling_mean + 1.96 * rolling_std / np.sqrt(window)
ci_lower = rolling_mean - 1.96 * rolling_std / np.sqrt(window)

fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(annual.index, rolling_mean, color='#E74C3C', linewidth=2)
ax.fill_between(annual.index, ci_lower, ci_upper, alpha=0.2, color='#E74C3C')
ax.set_title('全球气温10年滑动均值（含95%置信区间）')
```

**应用**：趋势+不确定性同时展示

---

### Slide 22｜双轴图 twinx：不同量纲共图

```python
fig, ax1 = plt.subplots(figsize=(12, 5))

# 左轴：气温距平
ax1.plot(years, temp_anomaly, color='#E74C3C', label='气温距平')
ax1.set_ylabel('温度距平 (°C)', color='#E74C3C')

# 右轴：CO2 浓度
ax2 = ax1.twinx()
ax2.plot(years, co2_ppm, color='#3498DB', label='CO2浓度')
ax2.set_ylabel('CO2 (ppm)', color='#3498DB')

fig.legend(loc='upper left', bbox_to_anchor=(0.12, 0.88))
```

**注意**：双轴图容易误导（两个Y轴范围任意缩放），需标注清楚

---

### Slide 23｜统计标注：显著性星号与 p 值

```python
from scipy import stats

# t检验：1990-2024 vs 1880-1920
recent = annual[annual.index >= 1990].values
early = annual[annual.index <= 1920].values
t_stat, p_value = stats.ttest_ind(recent, early)

# 在图上标注
ax.annotate('***', xy=(1990, 0.8), fontsize=16, ha='center')
ax.annotate(f'p = {p_value:.2e}', xy=(1990, 0.75), fontsize=9, ha='center')

# 画连接线
ax.plot([1900, 1900, 2010, 2010], [0.6, 0.7, 0.7, 0.6], 'k-', linewidth=1)
```

**星号规则**：* p<0.05, ** p<0.01, *** p<0.001

---

### Slide 24｜配色方案：色盲友好

```python
# 色盲友好的离散配色（推荐）
colorblind_palette = ['#0072B2', '#E69F00', '#009E73', '#CC79A7',
                      '#56B4E9', '#D55E00', '#F0E442']

# Seaborn 内置色盲友好
sns.set_palette('colorblind')

# 连续配色（适合热力图）
# 发散：'RdBu_r'（蓝=冷，红=暖）
# 顺序：'viridis'（色盲友好的连续色）
```

**原则**：不用红绿区分；用形状/线型辅助区分；打印黑白仍可读

---

### Slide 25｜发表级排版完整示例

```python
fig, ax = plt.subplots(figsize=(3.5, 2.8))  # 单栏宽度(inch)

ax.plot(years, temps, color='#0072B2', linewidth=1.2)
ax.fill_between(years, ci_low, ci_high, alpha=0.15, color='#0072B2')

ax.set_xlabel('Year', fontsize=9)
ax.set_ylabel('Temperature anomaly (°C)', fontsize=9)
ax.tick_params(labelsize=8)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('fig1.pdf', dpi=300, bbox_inches='tight')
plt.savefig('fig1.png', dpi=300, bbox_inches='tight')
```

**期刊要求**：PDF 矢量图优先；PNG 备用(300dpi)；单栏 3.5 inch 宽

---

### Slide 26｜AI 协作：发表级图表生成

**课堂练习**：

```
我需要为论文生成一张图，展示 1880-2024 年全球气温变暖趋势。
要求符合 Nature 期刊标准：
- 单栏宽度 3.5 inch
- 300 dpi
- 字号 8-9pt
- 白色背景，无网格
- 去掉顶部和右侧边框
- 颜色用 #E74C3C
- 加 10 年滑动平均线（黑色虚线）和 95% 置信区间（浅色填充）
- 标注 2016 年和 2023 年为历史最暖年
```

---

## Part 4：AI 辅助可视化表达（~7 张）

### Slide 27｜AI 辅助可视化：三轮迭代法

**Round 1（氛围层）**：
> 用气温距平数据画一张展示全球变暖趋势的图，科学感风格

**Round 2（约束层）**：
> 保持整体结构，按以下要求优化：
> 1. 正距平填充红色，负距平填充蓝色
> 2. 加 10 年滑动平均黑色虚线
> 3. 标注最暖和最冷年份
> 4. 中文标题和标签，300dpi

**Round 3（Inline Edit 微调）**：
> Cmd+K → "把 x 轴标签改为每 20 年显示一次；图例移到左上角"

---

### Slide 28｜AI 角色：设计顾问的三种用法

| 用法 | Prompt 示例 | 产出 |
|------|------------|------|
| 方案推荐 | "我想展示X，推荐图表类型" | 2-3种方案对比 |
| 视觉审查 | "这张图有什么问题？如何改进" | 改进建议清单 |
| 代码生成 | 详细约束 + 期刊要求 | 发表级代码 |

---

### Slide 29｜课堂综合案例：从数据到论文图

**全流程演示**（20分钟课堂实操）：

1. 加载 `global_temperature.csv`
2. 问 AI："这个数据适合画什么图？"（方案推荐）
3. 选择折线图+置信区间方案
4. Round 1 生成粗图
5. Round 2 加约束（配色/标注/分辨率）
6. Round 3 Inline Edit 微调（间距/标签/图例位置）
7. 导出 PDF + PNG

---

### Slide 30｜常见视觉审查问题

| 问题 | AI 可能犯的错 | 审查方法 |
|------|-------------|---------|
| 轴范围不合理 | Y 轴从 0 开始导致趋势不明显 | 看数据实际范围 |
| 颜色含义错误 | 暖色表示降温 | 检查图例 |
| 标注遮挡数据 | 文字覆盖关键点 | 调整位置/透明度 |
| 分辨率不足 | 保存时忘记 dpi=300 | 检查文件大小 |
| 中文乱码 | 未设置中文字体 | rcParams 检查 |

---

## Part 5：小结与实验

### Slide 31｜本讲知识速查

| 图表类型 | 适用场景 | 代码 |
|---------|---------|------|
| 折线图 | 时间趋势 | `plt.plot()` |
| 柱状图 | 类别对比 | `plt.bar()` |
| 直方图 | 分布形态 | `plt.hist()` |
| 箱线图 | 多组分布 | `plt.boxplot()` |
| 热力图 | 数值矩阵 | `sns.heatmap()` |
| 小提琴图 | 分布+密度 | `sns.violinplot()` |
| Pairplot | 多变量关系 | `sns.pairplot()` |
| 误差棒 | 不确定性 | `plt.errorbar()` |
| 置信区间 | 趋势+CI | `ax.fill_between()` |
| 双轴图 | 不同量纲 | `ax.twinx()` |

---

### Slide 32｜Vibe Coding 工具速查（本讲新增）

| 工具 | 本讲用法 |
|------|---------|
| AI 方案推荐 | "这个数据适合什么图？" |
| AI 视觉审查 | "这张图有什么问题？" |
| AI 代码生成 | 详细约束 → 发表级代码 |
| Inline Edit | Cmd+K 微调参数 |
| 三轮迭代 | 氛围→约束→微调 |

---

### Slide 33｜实验二：科研级数据可视化

**数据**：`global_temperature.csv`（NASA GISTEMP 全球气温距平，1880-2024）

| 任务 | 内容 | 核心技巧 | 分值 |
|------|------|---------|------|
| 任务1 | Matplotlib 基础图表 | 折线/柱状/多子图 | 20分 |
| 任务2 | Seaborn 高阶可视化 | 热力图/小提琴图/分面 | 25分 |
| 任务3 | 科研论文级图表 | 误差棒+置信区间+标注 | 30分 |
| 任务4 | AI 辅助三轮迭代 | 粗图→约束→发表级 | 25分 |

---

### Slide 34｜实验二 任务1：基础图表

用 `global_temperature.csv` 完成：
1. 年度气温距平折线图（正距平红色填充/负距平蓝色填充）
2. 各年代（1880s-2020s）平均气温距平柱状图（加数值标签）
3. 4 个季节的趋势折线图（2×2 多子图）
4. 全部图表中文标注 + 保存为 PNG(300dpi)

---

### Slide 35｜实验二 任务2：Seaborn 高阶

1. 热力图：月份(1-12) × 年代(1880s-2020s)的平均气温距平
2. 小提琴图：比较 1880-1950 vs 1951-2024 两个时期的月度气温距平分布
3. FacetGrid：四个季节各自的年度趋势分面图

---

### Slide 36｜实验二 任务3：科研论文级图表

产出一张符合发表标准的图：
1. 折线图展示 1880-2024 年趋势 + 10年滑动平均
2. 加 95% 置信区间（fill_between）
3. 标注最暖年份（2016/2023）
4. 加 t 检验结果标注（1880-1920 vs 1990-2024，p 值+星号）
5. 符合期刊要求：300dpi / 白底 / 无网格 / 色盲友好

---

### Slide 37｜实验二 任务4：AI 辅助迭代

**要求**：
- 选择任务1-3中的一张图，用 AI 从零生成
- 至少完成 3 轮迭代（氛围→约束→微调）
- 提交每轮 Prompt 截图 + 每轮图表截图
- 对比 Round 1 和 Round 3 的差异

**思考题（选做）**：
- AI 生成的配色方案是否色盲友好？你如何验证？
- 误差棒 vs 置信区间，分别适合什么场景？

---

### Slide 38｜课后作业

1. 完成实验二全部 4 个任务，提交实验报告
2. 保存至少 2 张发表级图表（PDF + PNG 各一份）

---

### Slide 39｜下讲预告

**第 3 讲：Spec-driven 协作建模与 Python 工程化**

- 前两讲的代码都是"一次性脚本"——能跑但不可靠
- 下讲解决：如何把原型变成实际可用的系统？
- AI 角色升级：从设计顾问 → 受控开发者

---

## 附录

### Slide 40｜Matplotlib 常用参数速查

| 参数 | 作用 | 推荐值 |
|------|------|--------|
| `figsize` | 图表尺寸(inch) | 单栏(3.5,2.8) 双栏(7,4) |
| `dpi` | 分辨率 | 300（发表）/ 100（屏幕） |
| `linewidth` | 线宽 | 1-2 pt |
| `markersize` | 标记大小 | 4-8 |
| `alpha` | 透明度 | 0.2-0.5（填充）/ 0.8-1（线） |
| `fontsize` | 字号 | 8-10（正文）/ 12（标题） |

---

### Slide 41｜Seaborn 常用函数速查

| 函数 | 用途 | 关键参数 |
|------|------|---------|
| `sns.heatmap()` | 热力图 | cmap, annot, center |
| `sns.violinplot()` | 小提琴图 | inner='quartile' |
| `sns.pairplot()` | 多变量 | diag_kind, corner |
| `sns.jointplot()` | 联合分布 | kind='hex'/'kde' |
| `sns.FacetGrid()` | 分面图 | col, col_wrap |
| `sns.kdeplot()` | 核密度 | fill=True |
| `sns.set_palette()` | 配色 | 'colorblind' |

---

### Slide 42｜科研图表 Checklist

- [ ] 分辨率 ≥ 300 dpi
- [ ] 字号 8-10pt（缩放后仍可读）
- [ ] 白色背景，无灰色网格
- [ ] 去掉顶部和右侧边框（spines）
- [ ] 配色色盲友好
- [ ] 坐标轴标签含单位
- [ ] 图例不遮挡数据
- [ ] 导出 PDF（矢量）+ PNG（位图备用）

---

### Slide 43｜色盲友好配色方案

**推荐离散配色（Wong 2011）**：

| 颜色 | 十六进制 | 用途 |
|------|---------|------|
| 蓝 | #0072B2 | 主数据线 |
| 橙 | #E69F00 | 第二数据线 |
| 绿 | #009E73 | 第三数据线 |
| 粉 | #CC79A7 | 第四数据线 |
| 浅蓝 | #56B4E9 | 填充/背景 |
| 红 | #D55E00 | 强调/警告 |

> 来源：Wong, B. (2011) "Points of view: Color blindness" Nature Methods

---

### Slide 44｜数据获取说明

**global_temperature.csv 来源**：
- NASA GISS Surface Temperature Analysis (GISTEMP v4)
- 下载：https://data.giss.nasa.gov/gistemp/
- 整理版：https://datahub.io/core/global-temp
- 许可：公共领域（Public Domain）

**数据结构**：

| 列名 | 类型 | 说明 |
|------|------|------|
| Source | str | 数据源：GISTEMP 或 GCAG |
| Year | int | 年份 1880-2024 |
| Month | int | 月份 1-12（月度数据）|
| Mean | float | 气温距平(°C)，基线1951-1980 |
