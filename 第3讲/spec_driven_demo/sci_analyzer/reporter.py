"""将实验数据和统计结果写成 Markdown 报告。"""

from collections.abc import Mapping
from pathlib import Path

import pandas as pd


def _format_stat(value: float | int) -> str:
    """格式化统计值，浮点数保留 4 位小数。"""
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def generate_report(
    df: pd.DataFrame,
    stats_result: Mapping[str, float | int],
    output_path: Path,
) -> Path:
    """生成实验数据分析 Markdown 报告。

    Args:
        df: 已完成清洗的实验数据，不会被本函数修改。
        stats_result: 上游模块计算完成的统计结果。
        output_path: 目标 Markdown 文件路径，必须以 `.md` 结尾。

    Returns:
        实际写入的报告路径。

    Raises:
        TypeError: `df` 不是 DataFrame 或 `stats_result` 不是映射类型。
        ValueError: 输出文件不是 `.md` 格式。
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df 必须是 pandas.DataFrame")
    if not isinstance(stats_result, Mapping):
        raise TypeError("stats_result 必须是 Mapping 类型")

    report_path = Path(output_path)
    if report_path.suffix.lower() != ".md":
        raise ValueError("output_path 必须以 .md 结尾")

    report_path.parent.mkdir(parents=True, exist_ok=True)
    column_lines = [f"- `{column}`: {dtype}" for column, dtype in df.dtypes.items()]
    stat_lines = [
        f"- `{name}`: {_format_stat(value)}"
        for name, value in stats_result.items()
    ]
    content = "\n".join(
        [
            "# 实验数据分析报告",
            "",
            "# 数据概览",
            f"- 行数：{df.shape[0]}",
            f"- 列数：{df.shape[1]}",
            "",
            "# 列信息",
            *column_lines,
            "",
            "# 统计结果",
            *(stat_lines or ["- 未提供统计结果"]),
            "",
        ]
    )
    report_path.write_text(content, encoding="utf-8")
    return report_path
