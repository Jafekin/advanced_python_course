'''
Author        Jiahui Chen 1946847867@qq.com
Date          2026-07-21 15:58:25
LastEditTime  2026-07-21 17:43:32
Description   

'''
import pandas as pd
import pytest

from sci_analyzer.reporter import generate_report


@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame({"样品": ["A", "B"], "浓度": [1.25, 2.5]})


def test_generate_report_writes_required_sections(tmp_path, sample_df) -> None:
    output_path = generate_report(
        sample_df,
        {"mean_concentration": 1.875, "sample_count": 2},
        tmp_path / "report.md",
    )

    content = output_path.read_text(encoding="utf-8")
    assert output_path.exists()
    assert "# 实验数据分析报告" in content
    assert "# 数据概览" in content
    assert "# 列信息" in content
    assert "# 统计结果" in content
    assert "1.8750" in content


def test_generate_report_does_not_mutate_dataframe(tmp_path, sample_df) -> None:
    original = sample_df.copy(deep=True)

    generate_report(sample_df, {"sample_count": 2}, tmp_path / "report.md")

    pd.testing.assert_frame_equal(sample_df, original)


def test_generate_report_creates_parent_directory(tmp_path, sample_df) -> None:
    output_path = tmp_path / "nested" / "reports" / "report.md"

    returned_path = generate_report(sample_df, {"sample_count": 2}, output_path)

    assert returned_path == output_path
    assert output_path.exists()


def test_generate_report_rejects_non_markdown_path(tmp_path, sample_df) -> None:
    with pytest.raises(ValueError, match=".md"):
        generate_report(sample_df, {"sample_count": 2}, tmp_path / "report.txt")


def test_generate_report_rejects_non_dataframe(tmp_path) -> None:
    with pytest.raises(TypeError, match="DataFrame"):
        generate_report([{"样品": "A"}], {"sample_count": 1}, tmp_path / "report.md")
