# 第一讲：Pandas 数据结构 × Vibe Coding 全景入门

## PPT 内容大纲（约 46 张 Slides）

---

### Slide 1｜封面

**标题**：Python 进阶 · 第 1 讲
**副标题**：Pandas 数据结构 × Vibe Coding 工具全景
**教师**：孙青 / 欧阳元新 · 计算机学院
**平台**：CloudStudio + CodeBuddy

---

### Slide 2｜本讲全景导航

**两条主线同步推进：**

| 知识线              | 工具线                         |
| ---------------- | --------------------------- |
| Pandas Series    | Vibe Coding 理念 + 两段式 Prompt |
| Pandas DataFrame | System Prompt & Rules       |
| 数据文件操作           | 上下文工程（四层级 + @引用）            |
| 数据可视化            | Inline Edit + Diff 审查       |
| —                | MCP 能力扩展                    |
| —                | Agent Skills                |

---

### Slide 3｜编程范式的三次革命

- 汇编 → C：从机器指令抽象到逻辑语句
- C → Python：从内存管理抽象到业务逻辑
- Python → **Vibe Coding**：从业务逻辑抽象到自然语言意图

每一次革命的本质，都是抽象层级的提升。

---

### Slide 4｜你的新身份：AI 指挥官

| 旧身份：代码工人   | 新身份：AI 指挥官 |
| ---------- | ---------- |
| 手写每一行代码    | 描述意图，AI 实现 |
| 靠记忆 API 文档 | 靠语言表达需求    |
| 调试是主要工作    | 审查和迭代是主要工作 |
| 知道怎么写      | 知道要什么、对不对  |

---

### Slide 5｜Vibe Coding 核心原则：先氛围后约束

**两段式 Prompt 节奏（最重要的方法论）：**

第一段：描述"感觉"（模糊意图）

```
帮我创建一组各城市空气质量指数（AQI）的 Pandas Series，展示基本统计信息
```

第二段：逐步收紧约束

```
在保持上面代码的前提下，增加：
1. 用城市名作为 index（北京、上海、广州等）
2. 打印 max、min、mean，并指出哪个城市空气最差
3. 所有变量名用英文，注释用中文
```

先定方向，再收紧约束，速度比一次性写完更快。

---

### Slide 6｜三个危险信号

| 危险信号            | 说明         | 正确做法               |
| --------------- | ---------- | ------------------ |
| 你开始手动改 AI 生成的代码 | 退回"代码工人"模式 | 用自然语言说清楚修改点，让 AI 改 |
| 你开始搜索语法细节       | 陷入旧思路时间黑洞  | 把问题描述给 AI，请它解释并给方案 |
| 你觉得描述需求比写代码慢    | 还在适应期      | 坚持"先目标、后约束"，速度会提升  |

---

### Slide 7｜CloudStudio + CodeBuddy 环境配置

**Step 1**：注册/登录 CloudStudio，创建 Python 工作区
**Step 2**：点击右侧 CodeBuddy 图标，选择 Craft 模式
**Step 3**：输入第一个 Prompt 初始化环境：

```
帮我配置一个 Python 数据分析环境，安装 pandas、matplotlib、openpyxl
安装skill:https://agenticskills.io/skills/jupyter-notebook，以后写notebook你要用它
```

**Step 4**：看到安装成功提示 → 环境就绪

---

### Slide 8｜Pandas 是什么

- **定位**：基于 NumPy 的高性能数据分析库
- **核心设计**：标签化数据访问（label-based），直觉友好
- **两大数据结构**：
  - `Series`：一维带标签的数组
  - `DataFrame`：二维带标签的表格
- **类比**：Series ≈ Excel 一列；DataFrame ≈ Excel 工作表

---

### Slide 9｜Series 特性：一维带标签的数组

**三件套之一：特性**

- 一维数组，每个值带标签（index）
- 标签让数据有"名字"，不再只靠位置
- 单一数据类型（dtype），与 NumPy 同构

**类比**：

| 特性       | Python list     | Pandas Series          |
| ---------- | --------------- | ---------------------- |
| 索引       | 0,1,2... 位置索引 | 自定义标签索引          |
| 数据类型   | 可混搭           | 统一 dtype，运算高效    |
| 统计方法   | 无内置           | `.mean()/.sum()/.describe()` 等 |

Series = 带标签的一维数组，是 DataFrame 取一列的返回类型。

---

### Slide 10｜Series 创建全景：三种方式

**三件套之二：操作全景**

```python
import pandas as pd

# 方式一：列表（自动整数索引）
s1 = pd.Series([89, 45, 67, 112, 78, 55, 93])

# 方式二：字典（键自动成为 index）—— 最推荐，语义清晰
s2 = pd.Series({'北京': 89, '上海': 45, '广州': 67, '成都': 112, '西安': 78})  # 某日各城市 AQI

# 方式三：常量广播
s3 = pd.Series(75, index=['北京', '上海', '广州'])  # 假设三城市优良线（AQI<=75）
```

**关键属性**：

```python
s2.values   # array([89, 45, 67, 112, 78])  数据值
s2.index    # Index(['北京','上海','广州','成都','西安'])  —— 标签
s2.dtype    # int64  数据类型
s2.name     # 可命名，便于区分
```

字典创建最常用，因为标签和数据一一对应，语义最清晰。

---

### Slide 11｜Series 索引与筛选

**三件套之二续：操作全景**

```python
s = pd.Series({'北京': 89, '上海': 45, '广州': 67, '成都': 112, '西安': 78, '深圳': 55, '杭州': 93})

# 标签索引
s['北京']                    # 89
s[['北京', '成都']]           # 取多值

# 切片
s['北京':'广州']             # 标签切片（闭区间）

# 条件筛选（布尔索引）
s[s > 75]                    # AQI > 75 的城市（轻度污染及以上）

# 排序
s.sort_values(ascending=False)  # 从高到低
```

如果 AI 生成的 Series 没有城市名索引，不要手动改，用 Round 2 Prompt 重新约束。

---

### Slide 12｜Series 统计方法与应用场景

**三件套之三：应用场景**

```python
s.sum()           # 总和
s.mean()          # 均值
s.std()           # 标准差
s.median()        # 中位数
s.min() / s.max() # 极值
s.idxmax()        # 最大值对应的标签
s.describe()      # 描述性统计摘要
s.value_counts()  # 各值频次（离散值有用）
s.quantile(0.25)  # 下四分位
```

**应用场景**：

- 单变量分析（如某国 24 个月贸易额的均值/波动）
- 找极值对应的日期（`idxmax` 告诉你哪天 AQI 最高）
- 按区间分组（`pd.cut` + `value_counts`）

---

### Slide 13｜Series 时间序列初探

**真实数据场景**：从航天贸易数据提取「日本进口 24 个月」Series

```python
# 读取后提取某一行为 Series
japan = pd.Series({c: row[c] for c in month_cols},
                  name='日本进口额（万元）')

# shift：本月与上月对比（环比）
japan - japan.shift(1)

# rolling：3 个月移动平均（平滑波动）
japan.rolling(3).mean()
```

应用场景：贸易额趋势、股价、销量等时间序列数据的环比与平滑。

---

### Slide 14｜DataFrame 特性：二维带标签的表格

**三件套之一：特性**

- 二维表格结构，每列可以是不同的 dtype
- 既有列索引（columns），又有行索引（index）
- 类比 Excel 工作表：一列就是一个 Series

```python
df = pd.DataFrame({
    '产品': ['耳机', '键盘', '鼠标', '显示器', '摄像头', '麦克风'],
    '一季度': [1200, 980, 1560, 2300, 890, 670],
    '二季度': [1450, 1120, 1820, 2100, 1040, 750],
    '三季度': [1680, 890, 2010, 2450, 960, 820]
})
df.shape        # (6, 4)
df.dtypes       # 各列数据类型
df.describe()   # 数值列统计摘要
df.head(3)      # 前3行
```

与 Series 的关系：DataFrame 取一列返回 Series，Series 是 DataFrame 的"积木"。

---

### Slide 15｜DataFrame 创建与属性

**三件套之二：操作全景**

```python
# 方式一：字典创建（最常用）
df = pd.DataFrame({
    '产品': ['耳机', '键盘', '鼠标', '显示器', '摄像头', '麦克风'],
    '一季度': [1200, 980, 1560, 2300, 890, 670],
    '二季度': [1450, 1120, 1820, 2100, 1040, 750],
    '三季度': [1680, 890, 2010, 2450, 960, 820]
})

# 方式二：从外部文件读取（最常用于真实数据）
df = pd.read_excel('航天进出口额.xlsx', sheet_name='Sheet0')
```

**关键属性**：

```python
df.shape          # (行数, 列数)
df.columns        # 列名
df.dtypes         # 各列类型
df.info()         # 内存与类型概览
df.describe()     # 数值列统计
```

---

### Slide 16｜DataFrame 列操作：选列与新增

```python
# 选列
df['产品']                               # 选单列 → Series
df[['产品', '一季度']]                    # 选多列 → DataFrame

# 新增列（向量化，禁止 for 循环）
df['季度合计'] = df['一季度'] + df['二季度'] + df['三季度']

# 新增列（条件映射）
import numpy as np
conditions = [df['季度合计'] >= 6000, df['季度合计'] >= 4000]
df['销售等级'] = np.select(conditions, ['A', 'B'], default='C')

# 删除列
df = df.drop(columns=['三季度'])
```

Rules 提醒：新增列用向量化，禁止 for 循环逐行处理。

---

### Slide 17｜DataFrame 行操作：筛选与定位

```python
# 条件筛选（布尔索引）
df[df['一季度'] > 1000]                          # 一季度销售额>1000 的产品
df[(df['一季度']>1000) & (df['二季度']>1000)]    # 多条件

# 精确定位
df.loc[0]                        # 按标签取行
df.iloc[1:3]                     # 按位置取行（切片）

# 排序
df.sort_values('季度合计', ascending=False)  # 降序
df.nlargest(10, '年度合计')      # 取 Top10
df.reset_index(drop=True)        # 重置索引
```

---

### Slide 18｜DataFrame 分组聚合：groupby

**真实数据场景**：航天贸易数据按方向（进口/出口）分组

```python
# 单列分组 + 多聚合
df.groupby('方向')[['年度合计']].agg(['sum', 'mean', 'count'])

# 多列分组
df.groupby(['方向', '国家'])['年度合计'].sum()

# 各国月度波动（std）
df_import['月标准差'] = df_import[month_cols].std(axis=1)
df_import.nlargest(5, '月标准差')
```

**应用场景**：

- 按类别汇总（进口/出口总额对比）
- 找波动最大的对象（哪些国家贸易最不稳定）

---

### Slide 19｜DataFrame 宽转长：melt

**问题**：航天数据是宽表（24 个月作列），时间序列分析需要长表

```python
# 宽转长
df_long = df.melt(
    id_vars=['方向', '国家'],      # 保留的标识列
    value_vars=month_cols,         # 要转换的列
    var_name='月份',               # 新列名
    value_name='贸易额'            # 值列名
)
```

| 宽表（1 行 24 列）     | 长表（24 行 3 列）         |
| --------------------- | ------------------------- |
| 国家 / 2022-01 / ...  | 国家 / 月份 / 贸易额       |
| 日本 / 2653 / ...     | 日本 / 2022-01 / 2653     |

应用场景：时间序列可视化、透视分析、Seaborn/Plotly 入参要求长格式。

---

### Slide 20｜工具线衔接①：System Prompt & Rules

**为什么需要 Rules？**

不定制 Rules，每次都像在和陌生人合作：AI 时而用中文注释、时而用英文；时而有错误处理、时而没有。

**在 `.codebuddy/rules/python-style.md` 中定义你的编码风格：**

```markdown
# Python 数据分析编码规范
- 变量名：英文，snake_case
- 注释：全部中文
- 禁止 for 循环逐行处理列（必须用向量化操作）
- DataFrame 修改必须用 .copy() 避免 SettingWithCopyWarning
- 可视化：必须设置中文字体和图表标题
```

Rules 配置好之后，AI 的每次输出都会带上你的风格。

---

### Slide 21｜工具线衔接②：上下文四个层级

| 层级      | 来源       | 特点        | 控制方式                   |
| ------- | -------- | --------- | ---------------------- |
| **系统层** | Rules 文件 | 自动加载，持久生效 | 编辑 `.codebuddy/rules/` |
| **会话层** | 当前对话历史   | 随对话积累     | 开新对话清空                 |
| **指令层** | `@` 引用   | 精准注入      | 主动选择文件/目录              |
| **隐式层** | 当前打开的文件  | 自动感知      | 切换/关闭文件                |

AI 输出质量取决于上下文精准度，上下文精准度 = 相关性 × (1 / 噪声量)。

---

### Slide 22｜@文件引用：让 AI 看到你的数据

**场景**：AI 需要看到你的实际数据结构才能生成准确代码

**操作步骤**：

1. 在对话框输入 `@`
2. 选择 `@Files` → 找到 `航天进出口额.xlsx`
3. 再写 Prompt：

```
@航天进出口额.xlsx 读取这个文件，解析指标列拆出方向/国家，
筛选进口额，按年度合计降序排列
```

最小上下文原则：信息不足，AI 会瞎猜；信息过多，AI 会混乱；信息精准，代码才能直接可用。

---

### Slide 23｜数据文件操作：多格式读写

**三件套之二：操作全景**

```python
# CSV（注意编码）
df = pd.read_csv('data.csv', encoding='utf-8-sig')
df.to_csv('out.csv', index=False, encoding='utf-8-sig')

# Excel（多 sheet）
df = pd.read_excel('航天进出口额.xlsx', sheet_name='Sheet0')
sheets = pd.ExcelFile('航天进出口额.xlsx').sheet_names  # 查看所有 sheet

# JSON（嵌套结构）
import json
with open('airports.json') as f:
    data = json.load(f)  # 嵌套字典
```

应用场景：CSV 跨平台交换；Excel 多 sheet 存原始+元数据；JSON 嵌套结构（如机场数据）。

---

### Slide 24｜数据文件操作：缺失值策略对比

**三件套之三：应用场景**

航天贸易数据月份列天然含缺失值（每月 2-7 个 NaN），演示两种策略：

```python
# 策略一：dropna（删除含缺失的行）
df_drop = df.dropna(subset=month_cols, how='any')  # 76→63 行

# 策略二：fillna 中位数（填充）
for col in month_cols:
    df[col] = df[col].fillna(df[col].median())     # 保持 76 行
```

| 策略          | 适用场景                       | 代价             |
| ------------- | ------------------------------ | ---------------- |
| dropna        | 缺失少、对完整性要求高         | 样本量减少       |
| fillna 中位数 | 缺失多、需保留样本、数据有偏态 | 引入估计偏差     |
| fillna 均值   | 数据近似正态分布               | 易被异常值拉偏   |

选择依据：看缺失比例 + 数据分布 + 业务能否容忍估计值。

---

### Slide 25｜数据文件操作：编码与写回

**编码问题实战**：

```python
# 错误：默认 utf-8，Excel 打开中文乱码
df.to_csv('out.csv', index=False)

# 正确：utf-8-sig 带 BOM，Excel 正确显示中文
df.to_csv('out.csv', index=False, encoding='utf-8-sig')

# 读取同理
df = pd.read_csv('out.csv', encoding='utf-8-sig')
```

**写回 Excel 多 sheet**：

```python
with pd.ExcelWriter('result.xlsx') as w:
    df_top10.to_excel(w, sheet_name='Top10', index=False)
    df_summary.to_excel(w, sheet_name='汇总', index=False)
```

Rules 强制：含中文的 CSV 必须加 `encoding='utf-8-sig'`。

---

### Slide 26｜工具线衔接③：Inline Edit + Diff 审查

**Inline Edit（行内编辑）**：在当前上下文中完成修改，不切换文件不切换窗口

| 操作      | 快捷键                         | 说明            |
| ------- | --------------------------- | ------------- |
| 唤起行内编辑  | `Cmd+K`（Mac）/ `Ctrl+K`（Win） | 在光标位置唤起 AI 编辑 |
| 接受修改    | 点击 Accept                   | 应用 AI 建议      |
| 拒绝修改    | 点击 Reject                   | 撤销 AI 建议      |
| 查看 Diff | 自动展示                        | 修改前后对比视图      |

**Diff 三步审查清单**：

1. 列名是否正确？和 CSV/Excel 一致？
2. 逻辑是否正确？筛选/排序方向？
3. 边界处理？空值、类型转换、编码？

每次 AI 修改后，先看 Diff 再点 Accept。

---

### Slide 27｜数据可视化：图表决策树

**三件套之一：什么时候用什么图**

| 分析目标     | 推荐图表   | Pandas/Matplotlib 方法        |
| ---------- | ---------- | ----------------------------- |
| 分布       | 直方图     | `plt.hist()` / `df.plot.hist()` |
| 对比       | 柱状图     | `plt.bar()` / `df.plot.bar()` |
| 关系       | 散点图     | `plt.scatter()` |
| 趋势       | 折线图     | `plt.plot()` / `df.plot()` |
| 分组分布   | 箱线图     | `plt.boxplot()` |

**决策口诀**：

- 看一个变量的形态，用直方图
- 比几个类别的多少，用柱状图
- 看两个变量的关联，用散点图
- 看随时间的变化，用折线图
- 比多组的分布，用箱线图

---

### Slide 28｜数据可视化：柱状图与折线图

```python
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei']

# 柱状图：进口 Top10 来源国对比
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(df_top10['国家'], df_top10['年度合计']/10000, color='steelblue')
ax.set_title('航天器及零件进口 Top10 来源国')
ax.set_ylabel('进口额（亿元）')
plt.xticks(rotation=30)

# 折线图：某国 24 个月趋势
fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(month_cols, japan_values, marker='o', markersize=4)
ax.set_title('日本进口月度趋势')
plt.xticks(rotation=45)
```

应用场景：柱状图做对比（Top10），折线图看趋势（时间序列）。

---

### Slide 29｜数据可视化：直方图与箱线图

```python
# 直方图：所有进口月度额的分布
plt.hist(all_values, bins=30, color='coral', edgecolor='white')

# 箱线图：Top5 国家月度分布对比
plt.boxplot(data, labels=df_top5['国家'].tolist(),
            flierprops={'marker':'o','color':'red'})
```

**图表元素配置**：

- 中文字体：`plt.rcParams['font.sans-serif']`
- 标题：`ax.set_title()`
- 轴标签：`ax.set_xlabel()` / `ax.set_ylabel()`
- 旋转标签：`plt.xticks(rotation=30)`
- 异常值标记：`flierprops`

应用场景：直方图看整体分布，箱线图比多组分布并标异常值。

---

### Slide 30｜数据可视化：多子图布局

```python
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

axes[0,0].bar(...)     # 柱状图
axes[0,1].plot(...)    # 折线图
axes[1,0].hist(...)    # 直方图
axes[1,1].boxplot(...) # 箱线图

plt.tight_layout()  # 自动调整间距
plt.show()
```

应用场景：一次呈现多个视角，对比分析（如贸易数据的对比/趋势/分布/分组四视图）。

---

### Slide 31｜可视化 Prompt 三轮迭代

**Round 1（氛围）**：

> 用 Matplotlib 画一个现代感的进口 Top10 柱状图，科技感配色

**Round 2（加约束）**：

> 保持科技感，按以下要求优化：1) 深色背景 #1a1a2e；2) 柱子蓝紫渐变；3) 添加数值标签；4) 中文字体

**Round 3（Inline Edit 细节）**：

> 选中 `width` 参数 → Cmd+K → "柱子间距调整为 0.5；x 轴标签旋转 30 度；保存为 PNG"

---

### Slide 32｜工具线衔接④：MCP 能力扩展

**MCP = Model Context Protocol（模型上下文协议）**

没有 MCP，AI 只能看你给它的文件。有了 MCP：

| MCP Server | AI 能做到               |
| ---------- | -------------------- |
| SQLite MCP | 直接查询数据库，生成匹配真实表结构的代码 |
| GitHub MCP | 读取 Issues、PR、提交记录    |
| Figma MCP  | 访问设计稿，生成匹配设计的代码      |
| 自定义 MCP    | 对接任何内部系统             |

AI 从"封闭空间的助手"变成"连接一切的 Agent"。

---

### Slide 33｜工具线衔接⑤：Agent Skills

**Skills = 给 AI 配的"固定招式/SOP"**

没有 Skills：每次都要重新交代规则，输出风格随机
有了 Skills：一遇到某类任务，自动按规定流程做

**SKILL.md 基础结构**：

```
my-skill/
├── SKILL.md          # 元数据 + 指令（必需）
└── 可选资源/
    ├── scripts/      # 可执行脚本
    ├── references/   # 参考文档
    └── assets/       # 模板文件
```

与 Rules 的区别：Rules 控制风格；Skills 封装流程（SOP）。
与 MCP 的区别：MCP 提供外部能力；Skills 规范执行流程。

---

### Slide 34｜工具线衔接⑥：自定义斜杠指令

**斜杠指令 = 把高频工作流封装成一个命令**

CodeBuddy 内置指令（直接可用）：

- `/cr` — 代码审查
- `/explain` — 代码解释
- `/fix` — 代码修复
- `/tests` — 生成单元测试
- `/rules` — 自动生成 Rules 文件

**自定义示例**：把"航天贸易分析+生成报告"封装为 `/trade-report`

```yaml
---
name: trade-report
description: "读取航天数据，解析指标，生成 Top10 报告"
---
# 执行流程
1. 读取 航天进出口额.xlsx
2. 解析指标列，筛选进口
3. 生成 Top10 柱状图保存为 PNG
4. 输出 进口Top10.csv
```

---

### Slide 35｜Vibe Coding 工具全景图（总结）

```
意图表达层：  先氛围后约束 → 两段式 Prompt → Inline Edit(Cmd+K)
风格控制层：  System Prompt → Rules（.codebuddy/rules/）→ Skills(SOP)
上下文层：    系统层(Rules) + 会话层 + 指令层(@引用) + 隐式层(打开文件)
能力扩展层：  MCP(外部数据源) → Agent Skills(封装流程) → 自定义斜杠指令
```

---

### Slide 36｜实验任务总览（三份真实数据集）

| 任务  | 数据集               | 大小    | 内容           | 核心技巧               | 分值  |
| --- | --- | --- | --- | --- | --- |
| 任务一 | `航天进出口额.xlsx` | 30KB  | 航天贸易进出口分析（柱状/折线/箱线） | 两段式 Prompt + @文件引用 | 25分 |
| 任务二 | `karate.gml`      | 4KB   | 空手道俱乐部社交网络分析 | Round 迭代 + Diff 审查 | 35分 |
| 任务三 | `airports.json`   | 8.5MB | 全球机场3D空间分布   | 自然语言描述 + 视角约束      | 40分 |

三份数据集均已放在 `实验一/` 目录：

- `航天进出口额.xlsx`（30KB，国家统计局海关总署月度贸易数据，含自然缺失值+24个月时间序列）
- `karate.gml`（4KB，Zachary 空手道俱乐部社交网络，34节点 x 78边）
- `airports.json`（8.5MB，全球约5万个机场的经纬度和海拔）

完成标准：每个任务至少2轮 Prompt 截图 + 运行结果截图 + 代码说明

---

### Slide 37｜实验任务一：航天贸易数据分析（航天进出口额.xlsx）

数据集：国家统计局海关总署「HS88章 航空器、航天器及零件」月度进出口额（76 行 × 29 列，含 42 个国家/地区，2022-01 ~ 2023-12 共 24 个月，单位万元）

**指标列结构**（需解析）：

```
进口额(人民币)_(HS88章)航空器、航天器及其零件_日本_当期
        ↑                    ↑              ↑     ↑
      方向                  商品大类        国家   类型
```

**Round 1（氛围层）**：

```
读取 航天进出口额.xlsx，展示数据基本信息，
解析指标列拆出方向和国家，清洗缺失值，
用柱状图、折线图和箱线图展示贸易分布
```

**Round 2（约束层）**：

```
在保持上面代码的前提下，按要求调整：
1. 解析指标列：用 split('_') 拆出方向、国家
2. 筛选进口额，计算各国 24 个月合计，取 Top10
3. 柱状图：Top10 进口来源国，加数值标签
4. 折线图：某国（如日本）24 个月趋势，加标题和轴标签
5. 箱线图：Top5 国家月度分布对比，红色标注异常值
6. 全部图表支持中文显示
```

完成标准：三类图表全部正确输出 + 提交至少2轮 Prompt 截图

---

### Slide 38｜实验任务二：社交网络可视化（karate.gml）

数据集：Zachary 空手道俱乐部社交网络（34成员 x 78关系）

背景：这个数据集记录了美国一所大学空手道俱乐部34名成员之间的社交关系。每条边代表两人在俱乐部外的社交联系。后来俱乐部因纠纷分裂成两个派系，成为社区发现算法的经典测试数据。

**Round 1（氛围层）**：

```
读取 karate.gml 文件，用 NetworkX 绘制社交网络图，
节点显示标签，用 spring_layout 布局
```

**Round 2（约束层）**：

```
在保持上面代码的前提下，增加以下分析：
1. 计算并打印图的节点数、边数、平均度数
2. 计算每个节点到其他所有节点的平均最短路径长度，
   用柱状图展示（x轴=节点ID，y轴=平均最短路径长度）
3. 绘制10号节点到其他可达节点的距离分布直方图
4. 在图上用红色高亮显示节点1到节点10之间的最短路径，
   其余边用灰色显示
5. 全部图表支持中文显示
```

Diff 审查要点：节点标签是否为整数（gml 默认字符串，需 relabel）；最短路径算法方向是否正确

完成标准：基本网络图 + 节点数/边数/平均度数 + 最短路径分析图 + 路径红色高亮 + 提交至少2轮 Prompt 截图

---

### Slide 39｜实验任务三：全球机场 3D 可视化（airports.json）

数据集：全球约5万个机场，嵌套JSON结构

```json
{
  "00AK": {
    "name": "Lowell Field",
    "lat": 59.949,
    "lon": -151.696,
    "elevation": 450
  }
}
```

注意：elevation 单位是英尺，需转米（x0.3048）

**Round 1（氛围层）**：

```
读取 airports.json，提取所有机场的纬度（lat）、经度（lon）、
海拔（elevation），用 Matplotlib 3D 散点图展示全球机场空间分布
```

**Round 2（约束层）**：

```
在保持上面代码的前提下，按要求调整：
1. 海拔从英尺转为米（1英尺=0.3048米）
2. 约束坐标轴范围：经度-200~200，纬度-75~75，海拔0~4000
3. 添加坐标轴标签（经度、纬度、海拔（米））
4. 视角设为仰角30度、方位角45度
5. 支持中文显示，加标题"全球机场分布3D图"
```

数据量大（5万点），建议散点 s=1, alpha=0.3

完成标准：JSON 解析正确 + 3D 散点图 + 海拔转换 + 轴范围/视角设置 + 提交至少2轮 Prompt 截图

---

### Slide 40｜本讲小结

**知识收获**：

- Pandas Series / DataFrame 核心结构与常用操作（含 groupby、melt、时间序列）
- 数据文件读写（CSV/Excel 多 sheet/JSON）与缺失值策略
- Matplotlib 可视化（柱状/折线/直方/箱线/多子图）+ 3D 图
- NetworkX 社交网络分析

**Vibe Coding 工具全景**：

- 两段式 Prompt（先氛围后约束）
- Rules，定义编码风格
- 上下文四层级 + @文件引用
- Inline Edit + Diff 审查
- MCP 能力扩展
- Agent Skills
- 自定义斜杠指令

---

### Slide 41｜课后作业

1. 完成实验一全部 3 个任务，提交实验报告
2. 为本课程项目创建 `.codebuddy/rules/python-style.md`，至少写 8 条规则

---

## 附录：Vibe Coding 关键词速查

| 术语           | 含义                          |
| ------------ | --------------------------- |
| Vibe Coding  | 用自然语言意图驱动 AI 生成代码的编程范式      |
| 两段式 Prompt   | 先描述感觉/氛围，再逐步加约束             |
| Rules        | 项目级规则文件，控制 AI 输出风格          |
| @文件引用        | 将文件内容注入 AI 上下文的操作（指令层）      |
| 最小上下文原则      | 信息精准 > 信息过多；相关性 × (1/噪声量)   |
| Inline Edit  | Cmd/Ctrl+K 在光标处唤起 AI 行内编辑   |
| Diff 审查      | 查看 AI 修改前后对比，先看后 Accept     |
| MCP          | 模型上下文协议，让 AI 连接外部数据源和工具     |
| Agent Skills | 给 AI 配置可复用 SOP 的模块化能力封装     |
| 斜杠指令         | 把高频工作流封装成 /命令 的快捷触发方式       |

## 附录：Pandas 常用方法速查

| 操作 | 代码 |
|---|---|
| 创建 Series | `pd.Series({'北京': 89, '上海': 45, ...})` |
| 创建 DataFrame | `pd.DataFrame({'产品': [...], '一季度': [...]})` |
| 读取 Excel | `pd.read_excel('f.xlsx', sheet_name='Sheet0')` |
| 选列 | `df['列名']` / `df[['列1','列2']]` |
| 条件筛选 | `df[df['方向'] == '进口额']` |
| 排序 | `df.sort_values('年度合计', ascending=False)` |
| Top N | `df.nlargest(10, '年度合计')` |
| 新增列 | `df['年度合计'] = df[month_cols].sum(axis=1)` |
| 分组聚合 | `df.groupby('方向').agg(['sum','mean'])` |
| 宽转长 | `df.melt(id_vars, value_vars, var_name, value_name)` |
| 缺失值填充 | `df['列'].fillna(df['列'].median())` |
| 写回 CSV | `df.to_csv('out.csv', index=False, encoding='utf-8-sig')` |
| 滚动窗口 | `s.rolling(3).mean()` |
| 滞后对比 | `s.shift(1)` |
