import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# === Parameters ===
URL1 = "http://www.ssb.no/statbank/sq/10112000"
URL2 = "http://www.ssb.no/statbank/sq/10112001"
HP_LAMBDA = 14400

# === Load and clean ===
df1 = pd.read_csv(URL1, sep=';', skiprows=2, encoding='latin1')
df2 = pd.read_csv(URL2, sep=';', skiprows=2, encoding='latin1') 

# Keep relevant columns
df1 = df1[['måned', 'Faste 2022-priser, sesongjustert (mill. kr)']]
df2 = df2[['måned', 'Faste 2022-priser, sesongjustert (mill. kr)']]
df1.columns = ['month', 'export']
df2.columns = ['month', 'import']
df1['month'] = pd.to_datetime(df1['month'], format='%YM%m')
df2['month'] = pd.to_datetime(df2['month'], format='%YM%m')
df1['export'] = pd.to_numeric(df1['export'], errors='coerce')
df2['import'] = pd.to_numeric(df2['import'], errors='coerce')
df1.dropna(inplace=True)
df2.dropna(inplace=True)
df1.set_index('month', inplace=True)
df2.set_index('month', inplace=True)

dfs = [df1, df2]
df_trade = dfs[0]
for df in dfs[1:]:
    df_trade = df_trade.merge(df, left_index=True, right_index=True)


df_trade['net_export']=df_trade['export']-df_trade['import']

# === HP filter to get gap ===
cycle, trend = sm.tsa.filters.hpfilter(df_trade['net_export'], lamb=HP_LAMBDA)
df_trade['nx_gap_pct'] = 100 * (df_trade['net_export'] - trend) / trend

# === Save outputs ===
df_trade[['net_export', 'nx_gap_pct']].to_csv("data/gap_net_export.csv")

# === Plot ===
plt.figure(figsize=(10, 5))
plt.plot(df_trade.index, df_trade['nx_gap_pct'], label='Net Export Gap (%)')
plt.axhline(0, color='black', linestyle='--', linewidth=1)
plt.title("Deviation in Net Export (HP filter λ=14400)")
plt.xlabel("Date")
plt.ylabel("Percent")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("data/net_export_gap_plot.png")
plt.show()
