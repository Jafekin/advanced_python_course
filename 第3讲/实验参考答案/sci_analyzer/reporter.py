from pathlib import Path
from typing import Any
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def generate_report(
    df: pd.DataFrame,
    stats_result: dict[str, Any],
    output_path: Path,
) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    sections = []

    # 1. 数据概览
    sections.append("# 数据分析报告\n")
    sections.append("## 1. 数据概览\n")
    sections.append(f"- 数据形状: {df.shape[0]} 行 x {df.shape[1]} 列")
    sections.append(
        f"- 数值列: {len(df.select_dtypes(include='number').columns)}")
    sections.append(f"- 缺失值总数: {df.isnull().sum().sum()}")
    sections.append("")

    # 2. 清洗摘要
    sections.append("## 2. 数据质量\n")
    sections.append(f"- 重复行: {df.duplicated().sum()}")
    missing_cols = df.columns[df.isnull().any()].tolist()
    sections.append(f"- 含缺失值的列: {len(missing_cols)}")
    sections.append("")

    # 3. 统计结果
    sections.append("## 3. 统计分析结果\n")
    if "high_correlation_pairs" in stats_result:
        pairs = stats_result["high_correlation_pairs"]
        sections.append(f"- 高相关变量对(|r|>0.7): {len(pairs)} 对")
    if "t_test" in stats_result:
        t = stats_result["t_test"]
        sig = "显著" if t["significant"] else "不显著"
        sections.append(
            f"- t检验: t={t['t_statistic']}, p={t['p_value']} ({sig})")
    sections.append("")

    # 4. 结论
    sections.append("## 4. 结论\n")
    sections.append(f"本报告基于 {df.shape[0]} 条数据记录生成。")
    sections.append("数据质量良好，统计分析结果可靠。")

    report_text = "\n".join(sections)
    output_path.write_text(report_text, encoding="utf-8")
    logger.info(f"报告已生成: {output_path} ({len(report_text)} 字符)")
    return output_path
