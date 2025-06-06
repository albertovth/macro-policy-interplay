import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# === Parameters ===
URL = "http://www.ssb.no/statbank/sq/10111999"
HP_LAMBDA = 14400

# === Load and clean ===
df = pd.read_csv(URL, sep=';', skiprows=2, encoding='latin1')

# Keep relevant columns
df = df[['måned', 'Faste 2022-priser, sesongjustert (mill. kr)']]
df.columns = ['month', 'investment']
df['month'] = pd.to_datetime(df['month'], format='%YM%m')
df['investment'] = pd.to_numeric(df['investment'], errors='coerce')
df.dropna(inplace=True)
df.set_index('month', inplace=True)

# === HP filter to get gap ===
cycle, trend = sm.tsa.filters.hpfilter(df['investment'], lamb=HP_LAMBDA)
df['i_gap_pct'] = 100 * (df['investment'] - trend) / trend

# === Save outputs ===
df[['investment', 'i_gap_pct']].to_csv("data/gap_investment.csv")

# === Plot ===
plt.figure(figsize=(10, 5))
plt.plot(df.index, df['i_gap_pct'], label='Investment Gap (%)')
plt.axhline(0, color='black', linestyle='--', linewidth=1)
plt.title("Deviation in Investment (HP filter λ=14400)")
plt.xlabel("Date")
plt.ylabel("Percent")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("data/investment_gap_plot.png")
plt.show()
