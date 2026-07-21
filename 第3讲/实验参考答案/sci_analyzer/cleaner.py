from typing import Any, Optional
import pandas as pd
import numpy as np
from scipy import stats as sp_stats
import logging

from .exceptions import CleanError

logger = logging.getLogger(__name__)


def clean_data(
    df: pd.DataFrame,
    drop_duplicates: bool = True,
    fill_strategy: str = "median",
    outlier_method: Optional[str] = None,
    outlier_threshold: float = 1.5,
) -> pd.DataFrame:
    result = df.copy()

    if drop_duplicates:
        before = len(result)
        result = result.drop_duplicates()
        removed = before - len(result)
        if removed > 0:
            logger.info(f"去除 {removed} 行重复数据")

    numeric_cols = result.select_dtypes(include="number").columns
    if fill_strategy == "median":
        result[numeric_cols] = result[numeric_cols].fillna(result[numeric_cols].median())
    elif fill_strategy == "mean":
        result[numeric_cols] = result[numeric_cols].fillna(result[numeric_cols].mean())
    elif fill_strategy == "zero":
        result[numeric_cols] = result[numeric_cols].fillna(0)

    if outlier_method:
        for col in numeric_cols:
            mask, _ = detect_outliers(result[col], method=outlier_method, threshold=outlier_threshold)
            result.loc[mask, col] = np.nan
        result[numeric_cols] = result[numeric_cols].fillna(result[numeric_cols].median())

    return result


def detect_outliers(
    series: pd.Series,
    method: str = "iqr",
    threshold: float = 1.5,
) -> tuple[pd.Series, dict[str, Any]]:
    values = series.dropna()
    if method == "iqr":
        Q1, Q3 = values.quantile(0.25), values.quantile(0.75)
        IQR = Q3 - Q1
        lower, upper = Q1 - threshold * IQR, Q3 + threshold * IQR
        mask = (series < lower) | (series > upper)
        info = {"method": "iqr", "Q1": Q1, "Q3": Q3, "IQR": IQR, "lower": lower, "upper": upper}
    elif method == "zscore":
        z = np.abs(sp_stats.zscore(values))
        z_full = pd.Series(np.nan, index=series.index)
        z_full[values.index] = z
        mask = z_full > threshold
        info = {"method": "zscore", "threshold": threshold}
    else:
        raise CleanError("series", f"不支持的方法: {method}")

    info["outlier_count"] = int(mask.sum())
    return mask, info
