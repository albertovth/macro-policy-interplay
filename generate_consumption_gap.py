import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# === Parameters ===
URL = "http://www.ssb.no/statbank/sq/10111998"
HP_LAMBDA = 14400

# === Load and clean ===
df = pd.read_csv(URL, sep=';', skiprows=2, encoding='latin1')

# Keep relevant columns
df = df[['måned', 'Faste 2022-priser, sesongjustert (mill. kr)']]
df.columns = ['month', 'consumption']
df['month'] = pd.to_datetime(df['month'], format='%YM%m')
df['consumption'] = pd.to_numeric(df['consumption'], errors='coerce')
df.dropna(inplace=True)
df.set_index('month', inplace=True)

# === HP filter to get gap ===
cycle, trend = sm.tsa.filters.hpfilter(df['consumption'], lamb=HP_LAMBDA)
df['c_gap_pct'] = 100 * (df['consumption'] - trend) / trend

# === Save outputs ===
df[['consumption', 'c_gap_pct']].to_csv("data/gap_consumption.csv")

# === Plot ===
plt.figure(figsize=(10, 5))
plt.plot(df.index, df['c_gap_pct'], label='Consumption Gap (%)')
plt.axhline(0, color='black', linestyle='--', linewidth=1)
plt.title("Deviation in Consumption (HP filter λ=14400)")
plt.xlabel("Date")
plt.ylabel("Percent")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("data/consumption_gap_plot.png")
plt.show()
