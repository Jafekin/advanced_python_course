# tasks.md

## Task：实现 `sci_analyzer/reporter.py`

### 公开接口

```python
def generate_report(
    df: pd.DataFrame,
    stats_result: Mapping[str, float | int],
    output_path: Path,
) -> Path:
    ...
```

### 功能要求

1. 校验 `df` 是 `pandas.DataFrame`，`stats_result` 是映射类型。
2. 校验输出路径后缀为 `.md`；必要时创建父目录。
3. 写出 UTF-8 Markdown 文件，包含四个一级标题：`# 实验数据分析报告`、`# 数据概览`、`# 列信息`、`# 统计结果`。
4. 数据概览至少包含行数、列数；列信息至少列出列名和数据类型。
5. `stats_result` 中的浮点数保留 4 位小数，整数按整数展示。
6. 返回最终写入的 `Path`，且不修改原始 `df`。

## 验收标准

- `python -m pytest spec_driven_demo/tests/test_reporter.py -q` 全部通过；
- 正常写报告、创建父目录、输入不变、错误后缀、错误输入类型均有测试；
- 人工审查没有 bare `except`、硬编码路径和 `print` 调试语句。
