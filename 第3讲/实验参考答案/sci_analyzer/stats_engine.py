from typing import Any
import pandas as pd
from scipy import stats as sp_stats
import logging

logger = logging.getLogger(__name__)


def run_statistics(
    df: pd.DataFrame,
    target_col: str = None,
    group_col: str = None,
) -> dict[str, Any]:
    result = {}
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    # 描述统计
    result["describe"] = df[numeric_cols].describe().to_dict()

    # 相关性矩阵
    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr()
        result["correlation"] = corr.to_dict()

        # 高相关对
        high_corr = []
        for i in range(len(corr)):
            for j in range(i + 1, len(corr)):
                r = corr.iloc[i, j]
                if abs(r) > 0.7:
                    high_corr.append((corr.index[i], corr.columns[j], round(r, 4)))
        result["high_correlation_pairs"] = high_corr

    # 分组对比 t 检验
    if target_col and group_col and group_col in df.columns:
        groups = df[group_col].unique()
        if len(groups) == 2:
            g1 = df[df[group_col] == groups[0]][target_col].dropna()
            g2 = df[df[group_col] == groups[1]][target_col].dropna()
            t_stat, p_val = sp_stats.ttest_ind(g1, g2)
            result["t_test"] = {
                "groups": list(groups),
                "t_statistic": round(t_stat, 4),
                "p_value": round(p_val, 6),
                "significant": p_val < 0.05,
            }

    return result
