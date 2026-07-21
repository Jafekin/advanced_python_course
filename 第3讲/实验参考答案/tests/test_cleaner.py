'''
Author        Jiahui Chen 1946847867@qq.com
Date          2026-07-21 16:09:14
LastEditTime  2026-07-21 17:02:30
Description   

'''
import pytest
from sci_analyzer.cleaner import clean_data, detect_outliers
from sci_analyzer.exceptions import CleanError


def test_clean_removes_duplicates(sample_df):
    result = clean_data(sample_df, drop_duplicates=True)
    assert len(result) == 4  # "A" 重复，去重后少1行


def test_clean_fills_missing(sample_df):
    result = clean_data(sample_df, fill_strategy="median")
    assert result["value"].isnull().sum() == 0


def test_clean_does_not_modify_input(sample_df):
    original_len = len(sample_df)
    _ = clean_data(sample_df)
    assert len(sample_df) == original_len  # 原始未被修改


@pytest.mark.parametrize("method,threshold,expected_min", [
    ("iqr", 1.5, 0),
    ("zscore", 2.0, 0),
])
def test_detect_outliers_methods(sample_df, method, threshold, expected_min):
    mask, info = detect_outliers(sample_df["value"].dropna(), method=method, threshold=threshold)
    assert mask.sum() >= expected_min
    assert "outlier_count" in info


def test_detect_outliers_invalid_method(sample_df):
    with pytest.raises(CleanError):
        detect_outliers(sample_df["value"], method="invalid")
