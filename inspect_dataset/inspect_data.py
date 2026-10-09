from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "olist_dataset"


for file in sorted(DATA_DIR.glob("*.csv")):

    print("\n" + "=" * 80)
    print(f"TABLE: {file.name}")
    print("=" * 80)

    df = pd.read_csv(file)

    print(f"Rows    : {len(df):,}")
    print(f"Columns : {len(df.columns)}")

    print("\nColumns:")
    for column in df.columns:
        print(f"  - {column}")

    print("\nData types:")
    print(df.dtypes.to_string())

    print("\nMissing values:")
    missing = df.isnull().sum()
    missing = missing[missing > 0]

    if missing.empty:
        print("  None")
    else:
        print(missing.to_string())

    print("\nFirst 2 rows:")
    print(df.head(2).to_string(index=False))