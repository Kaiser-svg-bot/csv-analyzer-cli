from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


class CSVDataset:
    """Represents a loaded CSV dataset and provides analytical methods."""

    def __init__(self, filepath: str | Path):
        self.filepath = Path(filepath)
        if not self.filepath.exists():
            raise FileNotFoundError(f"File not found: {self.filepath}")
        if self.filepath.suffix.lower() != ".csv":
            raise ValueError(f"File must be a .csv file, got: {self.filepath.suffix}")

        self.headers: list[str] = []
        self.rows: list[list[str]] = []
        self._load()

    def _load(self) -> None:
        """Loads and parses the CSV file."""
        with open(self.filepath, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            try:
                self.headers = [h.strip() for h in next(reader)]
            except StopIteration:
                self.headers = []
                self.rows = []
                return

            self.rows = [[val.strip() for val in row] for row in reader]

    @property
    def row_count(self) -> int:
        return len(self.rows)

    @property
    def col_count(self) -> int:
        return len(self.headers)

    def get_column_values(self, column_name: str) -> list[str]:
        """Returns all row values for a specific column."""
        if column_name not in self.headers:
            raise KeyError(f"Column '{column_name}' not found. Available: {self.headers}")
        col_idx = self.headers.index(column_name)
        return [row[col_idx] for row in self.rows if len(row) > col_idx]

    def column_stats(self, column_name: str) -> dict[str, Any]:
        """Calculates statistical metrics for a column."""
        values = self.get_column_values(column_name)

        missing_count = sum(1 for v in values if v == "" or v.lower() == "nan")
        non_empty = [v for v in values if v != "" and v.lower() != "nan"]

        stats: dict[str, Any] = {
            "total_count": len(values),
            "missing_count": missing_count,
            "missing_pct": round((missing_count / len(values)) * 100, 2) if values else 0.0,
            "is_numeric": False,
        }

        numeric_vals: list[float] = []
        for val in non_empty:
            try:
                numeric_vals.append(float(val))
            except ValueError:
                break

        if numeric_vals and len(numeric_vals) == len(non_empty):
            stats["is_numeric"] = True
            stats["min"] = min(numeric_vals)
            stats["max"] = max(numeric_vals)
            stats["mean"] = round(sum(numeric_vals) / len(numeric_vals), 2)
        else:
            stats["unique_count"] = len(set(non_empty))

        return stats

    def missing_summary(self) -> dict[str, int]:
        """Returns the count of missing values for every column."""
        summary = {}
        for col in self.headers:
            stats = self.column_stats(col)
            summary[col] = stats["missing_count"]
        return summary

    def head(self, n: int = 5) -> list[list[str]]:
        """Returns the first n rows."""
        return self.rows[:n]
