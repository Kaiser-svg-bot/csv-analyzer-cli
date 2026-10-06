from __future__ import annotations
import argparse
from src.csv_analyzer.core import CSVDataset

def main():
    parser = argparse.ArgumentParser(description="Analyze CSV files from the terminal.")
    
    # 1. Positional argument for filepath
    parser.add_argument("filepath", help="Path to the CSV file")
    
    # 2. Optional flag for summary (notice "-s")
    parser.add_argument("-s", "--summary", action="store_true", help="Print summary statistics")
    parser.add_argument("-c", "--stats", help="Show detailed stats for a specific column")
    # 3. Parse arguments
    args = parser.parse_args()

    # 4. Load dataset
    dataset = CSVDataset(args.filepath)

    # 5. Output results based on user's flags
    if args.summary:
        print(f"📊 Total Rows: {dataset.row_count}")
        print(f"📋 Columns ({dataset.col_count}): {', '.join(dataset.headers)}")
        print("\n❓ Missing Values per Column:")
        for col, count in dataset.missing_summary().items():
            print(f"  - {col}: {count}")
    elif args.stats:
        stats = dataset.column_stats(args.stats)
        print(f"📈 Stats for '{args.stats}':")
        for k, v in stats.items():
            print(f"  - {k}: {v}")
    else:
        print("📄 First 5 rows:")
        print(" | ".join(dataset.headers))
        print("-" * 30)
        for row in dataset.head(5):
            print(" | ".join(row))

if __name__ == "__main__":
    main()