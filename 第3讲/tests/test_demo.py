import pytest
import pandas as pd
import numpy as np
from pathlib import Path

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "name": ["A", "B", "C", "A", "D"],
        "value": [1.0, 2.0, np.nan, 1.0, 100.0],
        "category": ["x", "y", "x", "x", "y"]
    })

@pytest.fixture
def csv_file(tmp_path):
    f = tmp_path / "test.csv"
    f.write_text("name,value\nA,1\nB,2\nC,3")
    return f

def test_load_csv(csv_file):
    df = pd.read_csv(csv_file)
    assert len(df) == 3
    assert list(df.columns) == ["name", "value"]

def test_remove_duplicates(sample_df):
    result = sample_df.drop_duplicates()
    assert len(result) == 4

def test_load_nonexistent():
    with pytest.raises(Exception):
        pd.read_csv(Path("ghost_file.csv"))

@pytest.mark.parametrize("threshold,expected_outliers", [
    (1.5, 1),
    (3.0, 0),
])
def test_outlier_detection(sample_df, threshold, expected_outliers):
    values = sample_df["value"].dropna()
    Q1, Q3 = values.quantile(0.25), values.quantile(0.75)
    IQR = Q3 - Q1
    lower, upper = Q1 - threshold * IQR, Q3 + threshold * IQR
    outliers = values[(values < lower) | (values > upper)]
    assert len(outliers) == expected_outliers
