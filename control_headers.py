import pandas as pd

files = [
    "data/output_gap_monthly.csv",
    "data/kpi_cleaned.csv",
    "data/expected_inflation_cleaned.csv",
    "data/real_interest_rate_gap.csv",
    "data/gov_demand_gap.csv",
]

for file in files:
    print(f"\n=== {file} ===")
    try:
        df = pd.read_csv(file)
        print(df.head(3))
    except Exception as e:
        print("Error:", e)
