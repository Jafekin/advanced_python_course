# 第三讲：Spec-driven 协作建模与 Python 工程化

## PPT 内容大纲（约 44 张 Slides）

---

### Slide 1｜封面

**标题**：Python 进阶 · 第 3 讲
**副标题**：Spec-driven 协作建模 × Python 工程化
**教师**：孙青 / 欧阳元新 · 计算机学院
**平台**：CloudStudio + CodeBuddy

---

### Slide 2｜本讲全景导航

**从"能跑"到"可靠"：**

| 板块 | 内容 | AI 协作 |
|------|------|---------|
| Part 1 | Python 工程化基础 | AI 辅助重构 |
| Part 2 | Spec-driven 开发 | AI 受控实现 |
| Part 3 | 综合实战与小结 | 全流程演示 |

> AI 角色定位：**受控开发者**——Spec 定义约束 → AI 在边界内实现 → 人审查验收

---

### Slide 3｜承上启下：从脚本到系统

```
第1讲：数据处理（一次性脚本，能跑就行）
第2讲：数据可视化（一次性绘图，看完即弃）
第3讲：工程化（本讲）→ 把原型变成可靠、可复用、可维护的系统
```

**核心问题**：AI 生成的代码"能跑"，但能上线吗？能给别人用吗？半年后你还看得懂吗？

---

### Slide 4｜"能跑"≠"可靠"：三个致命缺陷

| 缺陷 | 举例 | 后果 |
|------|------|------|
| 无输入校验 | 文件路径写死，换数据就崩 | 只能在你电脑上跑 |
| 无错误处理 | 网络断了、文件不存在直接报错 | 用户看到 Traceback |
| 不可复现 | 全局变量满天飞，函数互相依赖 | 改一处全盘崩溃 |

**解决方案**：Python 工程化 + Spec-driven AI 协作

---

## Part 1：Python 工程化基础（~18 张）

### Slide 5｜本讲贯穿案例：科研实验数据管理工具

**目标**：把前2讲的散装分析脚本改造为一个完整 CLI 工具

```
输入：原始数据文件（CSV/Excel/JSON）
功能：自动加载 → 数据清洗 → 统计检验 → 一键生成论文级图表
输出：清洗报告 + 统计结果 + 发表级 PNG/PDF
```

**从这个案例出发，逐步学习工程化的每个环节。**

---

### Slide 6｜模块化组织：单文件 → 多文件

```
# 改造前（一个 300 行的 analysis.py）
import pandas as pd
df = pd.read_excel(...)
# ... 300 行混在一起 ...

# 改造后（结构化项目）
sci_analyzer/
├── __init__.py          # 包入口
├── loader.py            # 数据加载
├── cleaner.py           # 数据清洗
├── stats_engine.py      # 统计分析
├── visualizer.py        # 可视化
└── cli.py               # 命令行入口
```

---

### Slide 7｜包与模块：`__init__.py` 的作用

```python
# sci_analyzer/__init__.py
"""科研实验数据管理与分析工具"""

from .loader import load_data
from .cleaner import clean_data
from .stats_engine import run_statistics
from .visualizer import plot_results

__version__ = "0.1.0"
__all__ = ["load_data", "clean_data", "run_statistics", "plot_results"]
```

`__init__.py` = 包的"门面"：决定外部 import 时能看到什么

---

### Slide 8｜导入机制：绝对 vs 相对

```python
# 绝对导入（推荐：清晰明确）
from sci_analyzer.loader import load_data
from sci_analyzer.cleaner import clean_data

# 相对导入（包内部使用）
from .loader import load_data       # 同级目录
from ..utils import validate_path   # 上级目录
```

**选择原则**：外部调用用绝对导入；包内部用相对导入

---

### Slide 9｜AI 协作练习①：让 AI 拆分模块

**任务**：把一段 200 行的分析脚本拆分为模块化项目

```
@analysis_script.py
这个脚本完成了数据加载、清洗、统计和可视化。
请帮我拆分为 4 个模块（loader/cleaner/stats_engine/visualizer）+
一个 __init__.py，保持功能不变。
每个模块的函数加类型注解，导入关系清晰。
```

**审查要点**：循环导入？函数划分合理？接口是否统一？

---

### Slide 10｜类型注解：为什么 AI 生成的代码更需要它

```python
# 没有类型注解：这个函数接受什么？返回什么？
def process(data, config):
    ...

# 有类型注解：一目了然
def process(data: pd.DataFrame, config: dict[str, Any]) -> pd.DataFrame:
    ...
```

**三大好处**：
1. IDE 自动补全更精准
2. AI 生成的代码更容易审查
3. 团队协作减少沟通成本

---

### Slide 11｜typing 模块常用类型

```python
from typing import Optional, Union, Any
from pathlib import Path

def load_data(
    file_path: Path,
    sheet_name: Optional[str] = None,
    encoding: str = "utf-8"
) -> pd.DataFrame:
    """加载数据文件，支持 CSV/Excel/JSON"""
    ...

def detect_outliers(
    series: pd.Series,
    method: str = "iqr",
    threshold: float = 1.5
) -> tuple[pd.Series, dict[str, Any]]:
    """检测异常值，返回布尔掩码和统计信息"""
    ...
```

---

### Slide 12｜异常处理：try/except 层级设计

```python
def load_data(file_path: Path) -> pd.DataFrame:
    """加载数据，优雅处理各种错误"""
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    try:
        suffix = file_path.suffix.lower()
        if suffix == ".csv":
            return pd.read_csv(file_path, encoding="utf-8-sig")
        elif suffix in (".xlsx", ".xls"):
            return pd.read_excel(file_path)
        elif suffix == ".json":
            return pd.read_json(file_path)
        else:
            raise ValueError(f"不支持的文件格式: {suffix}")
    except UnicodeDecodeError:
        return pd.read_csv(file_path, encoding="gbk")
    except Exception as e:
        raise RuntimeError(f"加载失败: {e}") from e
```

---

### Slide 13｜自定义异常：让错误信息有意义

```python
class DataError(Exception):
    """数据处理相关错误的基类"""
    pass

class LoadError(DataError):
    """数据加载失败"""
    pass

class ValidationError(DataError):
    """数据校验失败"""
    def __init__(self, column: str, reason: str):
        self.column = column
        super().__init__(f"列'{column}'校验失败: {reason}")
```

**设计原则**：按业务分层，不要一个 Exception 打天下

---

### Slide 14｜上下文管理器：资源自动释放

```python
from contextlib import contextmanager
import time

@contextmanager
def timer(task_name: str):
    """计时上下文管理器"""
    start = time.time()
    yield
    elapsed = time.time() - start
    print(f"[{task_name}] 耗时 {elapsed:.2f}s")

# 使用
with timer("数据清洗"):
    df_clean = clean_data(df)
```

`with` 语句保证：无论是否出错，资源都会正确释放

---

### Slide 15｜AI 协作练习②：让 AI 添加异常处理

```
@sci_analyzer/loader.py
这个模块目前没有错误处理。请为每个函数添加：
1. 参数校验（文件是否存在、格式是否支持）
2. try/except 捕获 IO 和解析错误
3. 自定义 LoadError 异常
4. 用 logging 而非 print 输出错误信息
保持函数签名和返回值不变。
```

**Diff 审查重点**：异常是否过于宽泛（bare except）？错误信息是否足够定位问题？

---

### Slide 16｜测试：为什么 AI 代码更需要测试

**AI 生成代码的特点**：
- 看起来正确，但边界条件可能遗漏
- 你没写代码，所以对细节不熟悉
- 重构时没有安全网

**测试 = AI 代码的"验收标准"**：先写测试 → 再让 AI 实现 → 测试通过 = 验收成功

---

### Slide 17｜pytest 基础：断言与 fixture

```python
# tests/test_loader.py
import pytest
from sci_analyzer.loader import load_data
from sci_analyzer.exceptions import LoadError

def test_load_csv(tmp_path):
    """测试 CSV 加载"""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("name,value\nA,1\nB,2")
    df = load_data(csv_file)
    assert len(df) == 2
    assert list(df.columns) == ["name", "value"]

def test_load_nonexistent():
    """测试文件不存在的错误处理"""
    with pytest.raises(FileNotFoundError):
        load_data(Path("不存在的文件.csv"))
```

---

### Slide 18｜pytest 进阶：参数化测试

```python
@pytest.mark.parametrize("method,threshold,expected_count", [
    ("iqr", 1.5, 3),
    ("iqr", 3.0, 1),
    ("zscore", 3.0, 1),
    ("zscore", 2.0, 5),
])
def test_detect_outliers(sample_data, method, threshold, expected_count):
    """参数化测试异常值检测"""
    mask, info = detect_outliers(sample_data, method=method, threshold=threshold)
    assert mask.sum() == expected_count
```

**优势**：一组测试覆盖多种组合，代码简洁

---

### Slide 19｜测试驱动开发（TDD）：先写测试，再让 AI 实现

```
步骤1：你写测试（定义"什么是正确的"）
步骤2：让 AI 实现代码（让它通过测试）
步骤3：运行 pytest 验证
步骤4：不通过 → Round 2 Prompt 告知错误 → AI 修改
```

**TDD + AI = 最安全的开发方式**：
- 你控制"正确性标准"
- AI 负责"实现细节"
- pytest 做"裁判"

---

### Slide 20｜AI 协作练习③：TDD 实战

```
我已经写好了 5 个测试用例（见 tests/test_cleaner.py）。
请实现 sci_analyzer/cleaner.py 中的 clean_data 函数，
使所有测试通过。

函数签名：
def clean_data(df: pd.DataFrame, config: CleanConfig) -> pd.DataFrame

约束：
- 不修改原 DataFrame（用 .copy()）
- 支持 IQR 和 Z-score 两种异常值检测
- 缺失值填充策略从 config 读取
```

---

### Slide 21｜代码质量工具：ruff

```bash
# 安装
pip install ruff

# 检查（lint）
ruff check .

# 自动格式化
ruff format .

# 配置（pyproject.toml）
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W"]
```

**ruff = 替代 flake8 + isort + black 的一体化工具**（速度快 10-100x）

---

### Slide 22｜项目配置文件：pyproject.toml

```toml
[project]
name = "sci-analyzer"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = ["pandas>=2.0", "matplotlib>=3.7", "scipy>=1.10"]

[project.scripts]
sci-analyze = "sci_analyzer.cli:main"

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.ruff]
line-length = 100
```

一个文件管理：依赖、入口、测试配置、代码风格

---

## Part 2：Spec-driven 开发范式（~15 张）

### Slide 23｜从 Prompt 到 Spec：AI 协作的三个层级

| 层级 | 方式 | 适用场景 | AI 自由度 |
|------|------|---------|-----------|
| L1 | 两段式 Prompt | 单个函数/快速原型 | 高（自由发挥） |
| L2 | Rules 约束 | 代码风格统一 | 中（风格受限） |
| L3 | **Spec-driven** | 多模块工程 | **低（行为受限）** |

**进阶路径**：第1讲 L1 → 第2讲 L1+L2 → 本讲 **L3**

---

### Slide 24｜Spec-driven 核心思想

```
"先定义系统应该怎样，再让 AI 在约束内实现"
```

类比建筑：
- 两段式 Prompt = 口头告诉装修工"帮我搞好看点"
- Spec-driven = 给出建筑图纸 + 材料清单 + 验收标准

**三个关键文档**：
1. **Constitution**（硬约束）：不可违反的规则
2. **Context**（环境）：项目背景和依赖
3. **Tasks**（任务）：要做什么、做到什么程度

---

### Slide 25｜Speckit 工作流五步

```
constitution → specify → plan → tasks → implement
   定义硬约束    描述需求    生成计划   拆分任务    AI实现
```

| 步骤 | 你做什么 | AI 做什么 |
|------|---------|----------|
| constitution | 写不可违反的规则 | 读取并遵守 |
| specify | 描述功能需求 | 理解目标 |
| plan | 审查计划 | 生成模块划分 |
| tasks | 确认任务列表 | 拆分为可执行步骤 |
| implement | 审查代码 | 在约束内实现 |

---

### Slide 26｜Constitution：硬约束示例

```markdown
# constitution.md

## 不可违反的规则

1. 所有公开函数必须有类型注解
2. 所有公开函数必须有 docstring（Google style）
3. 不修改原始输入数据（必须 .copy()）
4. 错误处理：不允许 bare except，必须捕获具体异常
5. 测试覆盖：每个公开函数至少 2 个测试用例
6. 文件操作必须用 pathlib.Path，不用字符串拼接
7. 数值计算结果保留 4 位小数
8. 中文注释，英文变量名（snake_case）
```

---

### Slide 27｜Context：环境说明

```markdown
# context.md

## 项目环境

- Python 3.12+
- 核心依赖：pandas 2.x, matplotlib 3.x, scipy 1.x, seaborn 0.13+
- 测试框架：pytest 8.x
- 代码质量：ruff
- 数据来源：CSV/Excel/JSON 文件（可能含中文列名）
- 运行环境：CloudStudio（Linux 容器）

## 已有资产

- 第1讲清洗逻辑（可复用）
- 第2讲可视化模板（可复用）
- 航天进出口额.xlsx（测试数据）
- global_temperature.csv（测试数据）
```

---

### Slide 28｜Tasks：任务列表

```markdown
# tasks.md

## 实现任务

1. **loader 模块**：支持 CSV/Excel/JSON 加载，自动推断编码
2. **cleaner 模块**：重复值/缺失值/异常值处理，策略可配置
3. **stats_engine 模块**：描述统计 + t检验 + 相关性分析
4. **visualizer 模块**：基础图表 + 科研论文级图表
5. **cli 模块**：命令行入口，支持 --input --output --config
6. **tests/**：每个模块至少 5 个测试函数
7. **pyproject.toml**：项目配置完整

## 验收标准

- `pytest` 全绿
- `ruff check .` 无错误
- `sci-analyze --input data.csv --output results/` 能正确运行
```

---

### Slide 29｜实战：编写 speckit.md

```markdown
# speckit.md

@constitution.md
@context.md
@tasks.md

## 当前任务

实现 `sci_analyzer/cleaner.py` 模块：

### 功能要求
- `clean_data(df, config)` 主函数
- `remove_duplicates(df)` 去重
- `handle_missing(df, strategy)` 缺失值处理
- `detect_outliers(series, method, threshold)` 异常值检测

### 约束提醒
- 遵守 constitution.md 全部规则
- 不修改输入 df
- 所有阈值从 config 读取，不硬编码
```

---

### Slide 30｜AI 协作练习④：Spec-driven 实现

```
@speckit.md
请实现 sci_analyzer/cleaner.py 模块。

注意：
1. 严格遵守 constitution.md 中的所有规则
2. 先实现函数骨架，再填充逻辑
3. 每个函数开头做参数校验
4. 返回前打 log（用 logging，不用 print）
```

**审查清单**（比 Diff 三步更严格）：
- [ ] 类型注解完整？
- [ ] docstring 符合 Google style？
- [ ] 未修改原始输入？
- [ ] 异常处理具体？
- [ ] 阈值从 config 读取？

---

### Slide 31｜Spec vs Prompt：什么时候用哪个

| 场景 | 选择 | 理由 |
|------|------|------|
| 快速探索一个想法 | 两段式 Prompt | 灵活，快速迭代 |
| 写一个独立函数 | Prompt + Rules | 保证风格，但不限制实现 |
| 多模块项目开发 | Spec-driven | 需要一致性和约束 |
| 重构已有代码 | Spec-driven | 需要明确"改后应该怎样" |
| Bug 修复 | Prompt（带上下文） | 目标明确，不需要完整 Spec |

---

### Slide 32｜Constitution 的进阶用法

```markdown
# 项目级 Constitution（适用于所有模块）

## 安全规则
- 不允许 eval() / exec()
- 文件路径必须校验，禁止路径遍历
- 用户输入必须消毒

## 性能规则
- 循环内不允许 DataFrame 逐行操作
- 大于 10000 行的数据必须用 chunked 读取

## 兼容性规则
- 支持 Python 3.10+
- Windows/Mac/Linux 路径均兼容（用 pathlib）
```

---

### Slide 33｜从 Spec 到验收：完整循环

```
      ┌───────────────────────────────────────┐
      │                                       │
      ▼                                       │
  [Spec 定义] → [AI 实现] → [pytest 验证] ───┤
                                    │         │
                                    ▼ 不通过   │
                              [告知 AI 错误]──┘
                                    │
                                    ▼ 通过
                              [人工审查] → [合并]
```

**关键**：pytest 是自动裁判，减少人工审查负担

---

## Part 3：综合实战与小结（~7 张）

### Slide 34｜实战演示：完整工程化改造

**现场演示**（或录屏回放）：

1. 拿出第1讲的分析脚本（~100行混合代码）
2. 写 speckit.md（constitution + context + tasks）
3. 让 AI 按 Spec 拆分为 4 个模块
4. 写 3 个测试用例
5. 让 AI 实现，运行 pytest
6. 发现1个测试失败 → 告知 AI → 修复 → 全绿

**耗时对比**：手动重构 2h vs Spec-driven 30min

---

### Slide 35｜三讲 AI 角色演进总结

| 讲次 | AI 角色 | 核心操作 | 你的职责 |
|------|---------|---------|---------|
| 第1讲 | 编程搭档 | Prompt→生成→审查 | 描述需求 + Diff审查 |
| 第2讲 | 设计顾问 | 方案推荐→对比→选择 | 判断哪个方案更好 |
| 第3讲 | **受控开发者** | Spec约束→AI实现→验收 | 定义约束 + 写测试 |

**趋势**：AI 自由度递减，你的控制力递增，系统可靠性递增

---

### Slide 36｜知识点速查表

| 概念 | 代码 |
|------|------|
| 包结构 | `__init__.py` + 模块文件 |
| 绝对导入 | `from sci_analyzer.loader import load_data` |
| 类型注解 | `def f(x: int) -> str:` |
| Optional | `from typing import Optional` |
| 异常处理 | `try/except/else/finally` |
| 自定义异常 | `class MyError(Exception): ...` |
| 上下文管理器 | `with timer("task"):` |
| pytest | `def test_xxx(): assert ...` |
| 参数化 | `@pytest.mark.parametrize(...)` |
| ruff | `ruff check . && ruff format .` |
| pyproject.toml | 项目元数据+工具配置 |

---

### Slide 37｜Vibe Coding 工具速查（本讲新增）

| 工具 | 本讲用法 |
|------|---------|
| Spec-driven | 多模块项目的 AI 协作方式 |
| Constitution | 不可违反的硬约束 |
| speckit.md | @引用汇总约束+任务 |
| TDD + AI | 先写测试，AI 实现，pytest 裁判 |
| Inline Edit | 微调 AI 生成的模块代码 |

---

### Slide 38｜实验三：工程化改造实战

**任务**：将第1-2讲的实验代码改造为 Python 工程化项目

| 任务 | 内容 | 核心技巧 | 分值 |
|------|------|---------|------|
| 任务1 | 模块拆分 | 包结构+导入+__init__.py | 20分 |
| 任务2 | 类型注解+异常处理 | typing+try/except+自定义异常 | 25分 |
| 任务3 | 测试用例 | pytest+fixture+parametrize | 25分 |
| 任务4 | Spec-driven 新功能 | speckit.md+AI实现+验收 | 30分 |

---

### Slide 39｜实验三 任务1：模块拆分

将实验1/2的代码拆分为：

```
sci_analyzer/
├── __init__.py       # 导出公开接口
├── loader.py         # load_data(file_path) → DataFrame
├── cleaner.py        # clean_data(df, config) → DataFrame
├── stats_engine.py   # run_statistics(df) → dict
└── visualizer.py     # plot_results(df, output_dir)
```

**要求**：
- 每个模块独立可导入
- `from sci_analyzer import load_data, clean_data` 可用
- 无循环依赖

---

### Slide 40｜实验三 任务2：类型注解+异常处理

为 loader.py 和 cleaner.py 添加：
1. 所有函数的参数和返回值类型注解
2. 自定义异常类（LoadError, CleanError）
3. 完整的 try/except 链（文件不存在/编码错误/格式不支持）
4. 至少一个上下文管理器的使用

---

### Slide 41｜实验三 任务3：测试用例

```bash
pytest tests/ -v
```

要求：
- 至少 8 个测试函数（每模块至少 2 个）
- 使用 fixture 创建测试数据
- 至少 1 组参数化测试
- 包含正常路径和异常路径测试

---

### Slide 42｜实验三 任务4：Spec-driven 新功能

**新功能**：为 sci_analyzer 添加"自动报告生成"模块

1. 编写 speckit.md（含 constitution 规则引用）
2. 定义 `reporter.py` 的接口和行为
3. 让 AI 按 Spec 实现
4. 运行 pytest 验证
5. 提交 speckit.md + 实现代码 + 测试 + AI 对话截图

---

### Slide 43｜课后作业

1. 完成实验三全部 4 个任务
2. 确保 `pytest` 全绿、`ruff check .` 无报错
3. 提交项目完整目录结构 + speckit.md + AI 对话截图

---

### Slide 44｜下讲预告

**第 4 讲：NLP 基础与 Prompt 工程**

- 前3讲你已经能：处理数据 + 可视化 + 工程化
- 下讲进入 NLP 世界：理解语言模型 + 系统掌握 Prompt Engineering
- AI 角色：Prompt 设计师
