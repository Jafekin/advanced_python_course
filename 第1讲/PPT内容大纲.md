# 第一讲：Python 数据处理 × Vibe Coding

## PPT 内容大纲（约 42 张 Slides）

---

### Slide 1｜封面

**标题**：Python 进阶 · 第 1 讲
**副标题**：Python 数据处理 × Vibe Coding
**教师**：孙青 / 欧阳元新 · 计算机学院
**平台**：CloudStudio + CodeBuddy

---

### Slide 2｜本讲全景导航

**两条主线交替推进（知识点 → AI协作 → 知识点 → AI协作）：**

| 知识线 | AI 协作主线 |
|--------|-----------|
| Pandas Series 创建/索引/统计 | Vibe Coding 理念 + 两段式 Prompt |
| Pandas DataFrame 操作/分组聚合 | Rules + Diff 审查 |
| 数据文件读写与缺失值 | 上下文工程 + @文件引用 |
| 数据清洗与统计分析 | AI 辅助清洗 + 迭代纠错 |

> AI 角色定位：**编程搭档**——提示生成、迭代修改、代码纠错

---

### Slide 3｜编程范式的三次革命

- 汇编 → C：从机器指令抽象到逻辑语句
- C → Python：从内存管理抽象到业务逻辑
- Python → **Vibe Coding**：从业务逻辑抽象到自然语言意图

每一次革命的本质，都是抽象层级的提升。

---

### Slide 4｜你的新身份：AI 指挥官

| 旧身份：代码工人 | 新身份：AI 指挥官 |
|----------------|----------------|
| 手写每一行代码 | 描述意图，AI 实现 |
| 靠记忆 API 文档 | 靠语言表达需求 |
| 调试是主要工作 | 审查和迭代是主要工作 |
| 知道怎么写 | 知道要什么、对不对 |

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

| 危险信号 | 说明 | 正确做法 |
|---------|------|---------|
| 你开始手动改 AI 生成的代码 | 退回"代码工人"模式 | 用自然语言说清楚修改点，让 AI 改 |
| 你开始搜索语法细节 | 陷入旧思路时间黑洞 | 把问题描述给 AI，请它解释并给方案 |
| 你觉得描述需求比写代码慢 | 还在适应期 | 坚持"先目标、后约束"，速度会提升 |

---

### Slide 7｜CloudStudio + CodeBuddy 环境配置

**Step 1**：注册/登录 CloudStudio，创建 Python 工作区
**Step 2**：点击右侧 CodeBuddy 图标，选择 Craft 模式
**Step 3**：输入第一个 Prompt 初始化环境：

```
帮我配置一个 Python 数据分析环境，安装 pandas、matplotlib、openpyxl、seaborn
安装skill:https://agenticskills.io/skills/jupyter-notebook，以后写notebook你要用它
```

**Step 4**：看到安装成功提示 → 环境就绪

---

## Part 1：Pandas Series（含 AI 协作）

### Slide 8｜Pandas 是什么

- **定位**：基于 NumPy 的高性能数据分析库
- **核心设计**：标签化数据访问（label-based），直觉友好
- **两大数据结构**：
  - `Series`：一维带标签的数组
  - `DataFrame`：二维带标签的表格
- **类比**：Series ≈ Excel 一列；DataFrame ≈ Excel 工作表

---

### Slide 9｜Series 特性与创建

**特性**：一维数组，每个值带标签（index）；单一数据类型（dtype）

```python
import pandas as pd

# 方式一：列表（自动整数索引）
s1 = pd.Series([89, 45, 67, 112, 78, 55, 93])

# 方式二：字典（键自动成为 index）—— 最推荐
s2 = pd.Series({'北京': 89, '上海': 45, '广州': 67, '成都': 112, '西安': 78})

# 方式三：常量广播
s3 = pd.Series(75, index=['北京', '上海', '广州'])
```

**关键属性**：`s.values`、`s.index`、`s.dtype`、`s.name`

---

### Slide 10｜Series 索引与筛选

```python
s = pd.Series({'北京': 89, '上海': 45, '广州': 67, '成都': 112, '西安': 78})

# 标签索引
s['北京']                     # 89
s[['北京', '成都']]            # 取多值

# 切片（标签切片闭区间）
s['北京':'广州']

# 条件筛选（布尔索引）
s[s > 75]                     # AQI > 75 的城市

# 排序
s.sort_values(ascending=False)
```

---

### Slide 11｜Series 统计方法全景

```python
s.sum()           # 总和
s.mean()          # 均值
s.std()           # 标准差
s.median()        # 中位数
s.min() / s.max() # 极值
s.idxmax()        # 最大值对应的标签
s.describe()      # 描述性统计摘要
s.value_counts()  # 各值频次
s.quantile(0.25)  # 下四分位
```

**应用场景**：单变量分析（均值/波动）、找极值对应的索引、按区间分组

---

### Slide 12｜Series 时间序列初探

**真实数据场景**：从航天贸易数据提取「日本进口 24 个月」Series

```python
japan = pd.Series({c: row[c] for c in month_cols}, name='日本进口额（万元）')

# shift：本月与上月对比（环比）
japan - japan.shift(1)

# rolling：3 个月移动平均（平滑波动）
japan.rolling(3).mean()
```

应用场景：贸易额趋势、股价、销量等时间序列数据的环比与平滑。

---

### Slide 13｜AI 协作练习①：用 Prompt 完成 Series 分析

**任务**：用两段式 Prompt 让 AI 完成一个 Series 数据分析

**Round 1（氛围层）**：

```
帮我创建一个包含 7 个城市 AQI 数据的 Series，展示统计信息
```

**Round 2（约束层）**：

```
在保持上面代码的前提下：
1. 用城市名做 index，数据从给定字典读取
2. 打印 mean、std、idxmax，用中文注释解释含义
3. 用布尔索引筛选 AQI > 75 的城市
4. 变量名英文，注释中文
```

**审查要点**：AI 是否正确使用了 `idxmax()`？筛选条件方向对吗？

---

### Slide 14｜Rules：让 AI 记住你的编码风格

**为什么需要 Rules？** 不定制 Rules，每次都像在和陌生人合作。

**在 `.codebuddy/rules/python-style.md` 中定义：**

```markdown
# Python 数据分析编码规范
- 变量名：英文，snake_case
- 注释：全部中文
- 禁止 for 循环逐行处理列（必须用向量化操作）
- DataFrame 修改必须用 .copy() 避免 SettingWithCopyWarning
- 含中文的 CSV 必须加 encoding='utf-8-sig'
```

Rules = 系统层上下文，自动加载，AI 每次输出都带上你的风格。

---

## Part 2：Pandas DataFrame（含 AI 协作）

### Slide 15｜DataFrame 特性与创建

**特性**：二维表格，每列可以是不同 dtype；既有列索引又有行索引

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
```

与 Series 的关系：DataFrame 取一列返回 Series。

---

### Slide 16｜DataFrame 列操作与向量化

```python
# 选列
df['产品']                        # 单列 → Series
df[['产品', '一季度']]             # 多列 → DataFrame

# 新增列（向量化，禁止 for 循环）
df['季度合计'] = df['一季度'] + df['二季度'] + df['三季度']

# 条件映射
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
df[df['一季度'] > 1000]
df[(df['一季度'] > 1000) & (df['二季度'] > 1000)]

# 精确定位
df.loc[0]              # 按标签取行
df.iloc[1:3]           # 按位置取行

# 排序
df.sort_values('季度合计', ascending=False)
df.nlargest(3, '季度合计')    # Top 3

# 重置索引
df.reset_index(drop=True)
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

---

### Slide 19｜DataFrame 宽转长：melt

**问题**：航天数据是宽表（24 个月作列），时间序列分析需要长表

```python
df_long = df.melt(
    id_vars=['方向', '国家'],
    value_vars=month_cols,
    var_name='月份',
    value_name='贸易额'
)
```

| 宽表（1 行 24 列） | 长表（24 行 3 列） |
|-------------------|-------------------|
| 国家 / 2022-01 / ... | 国家 / 月份 / 贸易额 |

应用场景：时间序列可视化、Seaborn 入参要求长格式。

---

### Slide 20｜AI 协作练习②：DataFrame 分析

**任务**：描述分析目标，让 AI 生成 groupby 聚合代码

**Prompt 示例**：

```
@航天进出口额.xlsx
读取这个文件，按"方向"分组，计算各方向下所有国家的年度合计总额，
找出进口额最大的 Top5 国家，结果按降序排列
```

**审查清单（Diff 三步）**：
1. 列名是否和 Excel 一致？（指标列需要先解析）
2. 筛选方向是否正确？（"进口额" 还是 "进口"）
3. 排序方向是否正确？（ascending=False）

如果 AI 生成的代码列名不对 → **不要手动改**，用 Round 2 Prompt 纠正。

---

## Part 3：数据文件操作（含 AI 协作）

### Slide 21｜上下文工程：让 AI 看到你的数据

**上下文四层级**：

| 层级 | 来源 | 特点 | 控制方式 |
|------|------|------|---------|
| **系统层** | Rules 文件 | 自动加载 | 编辑 `.codebuddy/rules/` |
| **会话层** | 当前对话历史 | 随对话积累 | 开新对话清空 |
| **指令层** | `@` 引用 | 精准注入 | 主动选择文件/目录 |
| **隐式层** | 当前打开的文件 | 自动感知 | 切换/关闭文件 |

AI 输出质量 = 上下文精准度 = 相关性 × (1 / 噪声量)

---

### Slide 22｜@文件引用：精准注入数据结构

**操作步骤**：在对话框输入 `@` → 选择文件 → 写 Prompt

```
@航天进出口额.xlsx 读取这个文件，展示前5行和列名，
告诉我指标列的命名规则是什么
```

**最小上下文原则**：
- 信息不足 → AI 瞎猜
- 信息过多 → AI 混乱
- 信息精准 → 代码直接可用

---

### Slide 23｜数据文件操作：多格式读写

```python
# CSV（注意编码）
df = pd.read_csv('data.csv', encoding='utf-8-sig')
df.to_csv('out.csv', index=False, encoding='utf-8-sig')

# Excel（多 sheet）
df = pd.read_excel('航天进出口额.xlsx', sheet_name='Sheet0')
sheets = pd.ExcelFile('航天进出口额.xlsx').sheet_names

# JSON（嵌套结构）
import json
with open('airports.json') as f:
    data = json.load(f)
```

---

### Slide 24｜缺失值策略：dropna vs fillna

航天贸易数据月份列天然含缺失值（每月 2-7 个 NaN）：

```python
# 策略一：dropna
df_drop = df.dropna(subset=month_cols, how='any')   # 76→63 行

# 策略二：fillna 中位数
for col in month_cols:
    df[col] = df[col].fillna(df[col].median())      # 保持 76 行
```

| 策略 | 适用场景 | 代价 |
|------|---------|------|
| dropna | 缺失少、完整性要求高 | 样本量减少 |
| fillna 中位数 | 缺失多、数据有偏态 | 引入估计偏差 |
| fillna 均值 | 近似正态 | 易被异常值拉偏 |

---

### Slide 25｜AI 协作练习③：@引用 + 文件操作

**任务**：用 @文件引用让 AI 看到数据结构，生成清洗代码

**Prompt**：

```
@航天进出口额.xlsx
1. 读取这个文件，展示 shape 和前3行
2. 指标列格式为"进口额(人民币)_(HS88章)..._日本_当期"，
   用 split('_') 解析出方向和国家
3. 统计每列缺失值数量，选择合适策略填充
4. 变量名英文，注释中文
```

**对比演示**：有 @引用 vs 无 @引用，AI 生成代码的差异。

---

## Part 4：数据清洗与统计分析（含 AI 协作）

### Slide 26｜数据清洗全流程

```
原始数据 → 重复值检测 → 异常值识别 → 类型转换 → 缺失值处理 → 干净数据
```

**为什么数据清洗重要？**
- 真实数据从来不是干净的
- 机器学习 / 统计分析的结果质量取决于数据质量
- 做毕业论文时，60% 的时间花在数据清洗上

---

### Slide 27｜重复值检测与处理

```python
# 检测重复行
df.duplicated().sum()               # 重复行数量
df[df.duplicated(keep=False)]       # 显示所有重复行

# 删除重复行
df_clean = df.drop_duplicates()
df_clean = df.drop_duplicates(subset=['国家', '月份'], keep='first')
```

**场景**：数据合并后可能产生重复；多次导入追加时忘记去重。

---

### Slide 28｜异常值识别：IQR 法与 Z-score

```python
# IQR 法（适合偏态数据）
Q1 = df['贸易额'].quantile(0.25)
Q3 = df['贸易额'].quantile(0.75)
IQR = Q3 - Q1
lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
outliers = df[(df['贸易额'] < lower) | (df['贸易额'] > upper)]

# Z-score 法（适合近似正态）
from scipy import stats
z_scores = stats.zscore(df['贸易额'].dropna())
outliers = df[abs(z_scores) > 3]
```

**选择依据**：正态分布用 Z-score；偏态分布用 IQR。

---

### Slide 29｜数据类型转换

```python
# 查看类型
df.dtypes
df.info()

# 字符串 → 数值（处理无法转换的值）
df['金额'] = pd.to_numeric(df['金额'], errors='coerce')  # 无法转换→NaN

# 类型转换
df['年份'] = df['年份'].astype(int)
df['日期'] = pd.to_datetime(df['日期列'])

# 分类类型（节省内存）
df['方向'] = df['方向'].astype('category')
```

---

### Slide 30｜描述性统计全景

```python
# 单变量描述
df['贸易额'].describe()         # count/mean/std/min/25%/50%/75%/max
df['贸易额'].skew()             # 偏度（>0右偏，<0左偏）
df['贸易额'].kurtosis()         # 峰度（>0尖峰，<0平坦）

# 多变量概览
df.describe(include='all')      # 含分类列的统计
df.select_dtypes(include='number').describe()
```

**毕业论文场景**：先用 describe() 概览，再针对性深入。

---

### Slide 31｜相关性分析

```python
# 皮尔逊相关系数矩阵
corr_matrix = df[numeric_cols].corr()

# 查看某列与其他列的相关性
corr_matrix['年度合计'].sort_values(ascending=False)
```

**解读**：
- |r| > 0.8：强相关
- 0.5 < |r| < 0.8：中等相关
- |r| < 0.3：弱相关

> 相关 ≠ 因果，仅说明线性关联程度

---

### Slide 32｜AI 协作练习④：完整数据清洗

**任务**：描述清洗需求，让 AI 完成完整清洗流程

**Prompt**：

```
@航天进出口额.xlsx
对这个数据做完整的数据清洗：
1. 检查并报告重复行数量
2. 解析指标列，提取方向和国家
3. 用 IQR 法识别贸易额中的异常值，打印异常值所在行
4. 用中位数填充缺失值
5. 输出清洗报告：原始行数、清洗后行数、填充了多少个缺失值
```

**迭代要点**：如果 AI 的异常值判断有误，用自然语言纠正——不要手动改代码。

---

## Part 5：小结与实验

### Slide 33｜Inline Edit：行内修改利器

**操作**：`Cmd+K`（Mac）/ `Ctrl+K`（Win）在光标位置唤起 AI 编辑

**适用场景**：
- 修改一个参数值（阈值、列名、排序方向）
- 添加一行代码（打印某变量、添加注释）
- 不需要开新对话，在当前文件内完成

**Diff 三步审查清单**：
1. 列名是否正确？
2. 逻辑是否正确？
3. 边界处理？

每次 AI 修改后，先看 Diff 再点 Accept。

---

### Slide 34｜本讲知识速查

| 操作 | 代码 |
|------|------|
| 创建 Series | `pd.Series({'北京': 89, ...})` |
| 创建 DataFrame | `pd.DataFrame({...})` |
| 读 Excel | `pd.read_excel('f.xlsx', sheet_name=...)` |
| 条件筛选 | `df[df['方向'] == '进口额']` |
| Top N | `df.nlargest(10, '年度合计')` |
| 分组聚合 | `df.groupby('方向').agg(...)` |
| 宽转长 | `df.melt(id_vars, value_vars, ...)` |
| 缺失值 | `df.fillna(df.median())` |
| 重复值 | `df.drop_duplicates()` |
| 异常值 IQR | `Q1 - 1.5*IQR ~ Q3 + 1.5*IQR` |
| 相关性 | `df.corr()` |

---

### Slide 35｜Vibe Coding 工具速查

| 工具 | 作用 | 本讲用法 |
|------|------|---------|
| 两段式 Prompt | 先氛围后约束 | Series/DataFrame 分析 |
| Rules | 锁定 AI 输出风格 | python-style.md |
| @文件引用 | 精准注入数据结构 | 读取 Excel 数据 |
| Inline Edit | 行内修改 | 改参数/加注释 |
| Diff 审查 | Accept 前检查 | 三步清单 |
| 上下文四层级 | 理解 AI 信息来源 | 系统/会话/指令/隐式 |

---

### Slide 36｜实验一：航天贸易数据处理全流程

**数据**：`航天进出口额.xlsx`（76行×29列，42个国家/地区，2022-2023共24个月）

| 任务 | 内容 | 核心技巧 | 分值 |
|------|------|---------|------|
| 任务1 | 数据加载与探索 | @文件引用 + read_excel | 15分 |
| 任务2 | 指标列解析与数据清洗 | 两段式 Prompt 迭代 | 30分 |
| 任务3 | 分组聚合与统计分析 | groupby + describe | 30分 |
| 任务4 | AI 辅助数据处理 | 至少3轮 Prompt 截图 | 25分 |

---

### Slide 37｜实验一 任务1：数据加载与探索

```
@航天进出口额.xlsx
读取这个 Excel 文件，完成以下探索：
1. 打印 shape、columns、dtypes
2. 展示前5行
3. 统计每列缺失值数量
4. 说明这个数据集的结构特点
```

完成标准：正确读取 + 结构描述准确 + Prompt 截图

---

### Slide 38｜实验一 任务2：指标列解析与清洗

**指标列结构**：`进口额(人民币)_(HS88章)航空器、航天器及其零件_日本_当期`

```
Round 1：读取数据，尝试解析指标列，拆出方向和国家
Round 2：处理缺失值（选择 dropna 或 fillna 并说明理由）
Round 3：检测异常值，输出清洗报告
```

完成标准：正确解析 + 缺失值策略合理 + 清洗报告完整

---

### Slide 39｜实验一 任务3：统计分析

在清洗后的数据上完成：
1. 按方向分组计算总额
2. 进口 Top10 来源国（年度合计降序）
3. 各国月度贸易额的标准差（找波动最大的国家）
4. 进口/出口总额的相关性分析

---

### Slide 40｜实验一 任务4：AI 辅助全流程

**要求**：
- 全程使用 Vibe Coding 方式完成（不手写代码）
- 提交至少 3 轮 Prompt 迭代的截图
- 每轮标注：氛围层 or 约束层？AI 生成的代码哪里对、哪里需纠正？

**思考题（选做）**：
- 航天数据缺失值用 dropna 还是 fillna？各适合什么场景？
- @文件引用 vs 直接贴数据描述，哪种方式让 AI 生成的代码更准确？

---

### Slide 41｜课后作业

1. 完成实验一全部 4 个任务，提交实验报告
2. 为本课程项目创建 `.codebuddy/rules/python-style.md`，至少包含 8 条规则

---

### Slide 42｜下讲预告

**第 2 讲：数据高阶可视化与 AI 辅助表达**

- 如何把今天分析的结果转化为可信的视觉表达？
- Matplotlib 进阶 + Seaborn 高阶 + 科研论文图表
- AI 角色升级：从编程搭档 → 设计顾问
