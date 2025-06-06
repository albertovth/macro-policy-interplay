import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# === Parameters ===
URL = "http://www.ssb.no/statbank/sq/10111974"
HP_LAMBDA = 14400

# === Load and clean ===
df = pd.read_csv(URL, sep=';', skiprows=2, encoding='latin1')

# Keep relevant columns
df = df[['måned', 'Faste 2022-priser, sesongjustert (mill. kr)']]
df.columns = ['month', 'gov_demand']
df['month'] = pd.to_datetime(df['month'], format='%YM%m')
df['gov_demand'] = pd.to_numeric(df['gov_demand'], errors='coerce')
df.dropna(inplace=True)
df.set_index('month', inplace=True)

# === HP filter to get gap ===
cycle, trend = sm.tsa.filters.hpfilter(df['gov_demand'], lamb=HP_LAMBDA)
df['g_gap_pct'] = 100 * (df['gov_demand'] - trend) / trend

# === Save outputs ===
df[['gov_demand', 'g_gap_pct']].to_csv("data/gov_demand_gap.csv")

# === Plot ===
plt.figure(figsize=(10, 5))
plt.plot(df.index, df['g_gap_pct'], label='Government Demand Gap (%)')
plt.axhline(0, color='black', linestyle='--', linewidth=1)
plt.title("Deviation in Government Demand (HP filter λ=14400)")
plt.xlabel("Date")
plt.ylabel("Percent")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("data/gov_demand_gap_plot.png")
plt.show()
