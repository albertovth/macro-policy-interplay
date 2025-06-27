import pandas as pd

# Load CSV with correct separator and decimal
df = pd.read_csv("data/forventet_inflasjon.csv", sep=";", decimal=".")

# Rename and parse dates
df.columns = ["date", "kpi_now", "kpi_2y_exp", "kpi_5y_exp", "target"]
df["date"] = pd.to_datetime(df["date"], format="%d.%m.%Y")
df.set_index("date", inplace=True)

# Ensure values are numeric
df = df.apply(pd.to_numeric, errors="coerce")

# Create full monthly index using *month end* to align with quarterly dates
monthly_index = pd.date_range(start=df.index.min(), end=df.index.max(), freq="M")

# Reindex and interpolate
monthly_df = df.reindex(monthly_index).interpolate(method="linear", limit_direction="both")
monthly_df.index.name = "date"

# Save to CSV
monthly_df.to_csv("data/expected_inflation_monthly.csv")

# Show preview
print("Monthly data shape:", monthly_df.shape)
print(monthly_df.head(12))

