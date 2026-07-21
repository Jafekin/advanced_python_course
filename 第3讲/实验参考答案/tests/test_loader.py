'''
Author        Jiahui Chen 1946847867@qq.com
Date          2026-07-21 16:09:14
LastEditTime  2026-07-21 17:02:51
Description   

'''
import pytest
from pathlib import Path
from sci_analyzer.loader import load_data


def test_load_csv(csv_file):
    df = load_data(csv_file)
    assert len(df) == 3
    assert "name" in df.columns


def test_load_excel(excel_file):
    df = load_data(excel_file)
    assert len(df) == 2
    assert list(df.columns) == ["a", "b"]


def test_load_nonexistent():
    with pytest.raises(FileNotFoundError):
        load_data(Path("ghost.csv"))


def test_load_unsupported_format(tmp_path):
    f = tmp_path / "test.txt"
    f.write_text("hello")
    with pytest.raises(ValueError, match="不支持的格式"):
        load_data(f)
