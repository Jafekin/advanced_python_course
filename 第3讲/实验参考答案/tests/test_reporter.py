'''
Author        Jiahui Chen 1946847867@qq.com
Date          2026-07-21 16:09:14
LastEditTime  2026-07-21 17:02:56
Description   

'''
import pytest
import pandas as pd
from sci_analyzer.reporter import generate_report


@pytest.fixture
def report_input():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    stats = {"high_correlation_pairs": [("a", "b", 0.99)], "t_test": {"t_statistic": 2.5, "p_value": 0.02, "significant": True}}
    return df, stats


def test_report_generates_file(report_input, tmp_path):
    df, stats = report_input
    out = tmp_path / "report.md"
    result = generate_report(df, stats, out)
    assert result.exists()
    assert result.stat().st_size > 100


def test_report_contains_sections(report_input, tmp_path):
    df, stats = report_input
    out = tmp_path / "report.md"
    generate_report(df, stats, out)
    content = out.read_text()
    assert "数据概览" in content
    assert "统计分析" in content
    assert "结论" in content


def test_report_empty_stats(tmp_path):
    df = pd.DataFrame({"x": [1, 2]})
    out = tmp_path / "report.md"
    result = generate_report(df, {}, out)
    assert result.exists()
