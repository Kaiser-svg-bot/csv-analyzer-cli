from __future__ import annotations

import pytest
from pathlib import Path
from src.csv_analyzer.core import CSVDataset


@pytest.fixture
def sample_csv(tmp_path: Path) -> Path:
    """Fixture that creates a temporary sample CSV file for tests."""
    csv_file = tmp_path / "students.csv"
    content = (
        "name,age,marks\n"
        "Alice,20,85.5\n"
        "Bob,22,90.0\n"
        "Charlie,21,\n"
        "David,,78.0\n"
    )
    csv_file.write_text(content)
    return csv_file


def test_load_dataset(sample_csv: Path):
    ds = CSVDataset(sample_csv)
    assert ds.row_count == 4
    assert ds.col_count == 3
    assert ds.headers == ["name", "age", "marks"]


def test_missing_summary(sample_csv: Path):
    ds = CSVDataset(sample_csv)
    missing = ds.missing_summary()
    assert missing["name"] == 0
    assert missing["age"] == 1
    assert missing["marks"] == 1


def test_column_stats_numeric(sample_csv: Path):
    ds = CSVDataset(sample_csv)
    stats = ds.column_stats("marks")
    assert stats["is_numeric"] is True
    assert stats["min"] == 78.0
    assert stats["max"] == 90.0
    assert stats["mean"] == 84.5
    assert stats["missing_count"] == 1


def test_head(sample_csv: Path):
    ds = CSVDataset(sample_csv)
    first_two = ds.head(2)
    assert len(first_two) == 2
    assert first_two[0] == ["Alice", "20", "85.5"]


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        CSVDataset("non_existent_file.csv")


def test_invalid_extension(tmp_path: Path):
    txt_file = tmp_path / "test.txt"
    txt_file.write_text("hello")
    with pytest.raises(ValueError):
        CSVDataset(txt_file)
