import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import os


# Ensure output folder exists
os.makedirs("data", exist_ok=True)


# === Parameters ===
URL = "http://www.ssb.no/statbank/sq/10111961"
HP_LAMBDA = 14400

# === Load and clean ===
df = pd.read_csv(URL, sep=';', skiprows=2, encoding='latin1')

# DEBUG: show raw columns
print("Raw columns:", df.columns.tolist())

# Select relevant columns
df = df[['måned', 'Faste 2022-priser, sesongjustert (mill. kr)']]
df.columns = ['month', 'gdp']

# Parse month format like "2016M01" into datetime
df['month'] = pd.to_datetime(df['month'], format='%YM%m')
df['gdp'] = pd.to_numeric(df['gdp'], errors='coerce')
df.dropna(inplace=True)
df.set_index('month', inplace=True)

# DEBUG: show cleaned data
print("Preview of parsed data:")
print(df.head(10))
print("\nData shape:", df.shape)
print("Any missing values?\n", df.isna().sum())

# === Apply HP filter ===
cycle, trend = sm.tsa.filters.hpfilter(df['gdp'], lamb=HP_LAMBDA)
df['output_gap_pct'] = 100 * (df['gdp'] - trend) / trend

# === Save output ===
df.to_csv("data/output_gap_monthly.csv")

# === Plot ===
plt.figure(figsize=(10, 5))
plt.plot(df.index, df['output_gap_pct'], label='Output Gap (%)')
plt.axhline(0, color='black', linestyle='--', linewidth=1)
plt.title("Estimated Output Gap (Monthly, HP filter λ=14400)")
plt.xlabel("Date")
plt.ylabel("Percent")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("data/output_gap_monthly.png")
plt.show()
