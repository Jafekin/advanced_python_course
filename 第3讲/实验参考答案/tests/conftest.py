import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "name": ["A", "B", "C", "A", "D"],
        "value": [1.0, 2.0, np.nan, 1.0, 100.0],
        "category": ["x", "y", "x", "x", "y"],
    })


@pytest.fixture
def csv_file(tmp_path):
    f = tmp_path / "test.csv"
    f.write_text("name,value\nA,1\nB,2\nC,3", encoding="utf-8-sig")
    return f


@pytest.fixture
def excel_file(tmp_path):
    f = tmp_path / "test.xlsx"
    pd.DataFrame({"a": [1, 2], "b": [3, 4]}).to_excel(f, index=False)
    return f
