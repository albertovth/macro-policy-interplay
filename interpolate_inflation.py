import pandas as pd

# === Last inn data
df = pd.read_csv("data/kpi_cleaned.csv", parse_dates=["month"])

# === Behold bare relevante kolonner
df = df[["month", "inflation_pct"]]

# === Kast rader uten verdi (må ha tall for å interpolere fra)
df = df.dropna(subset=["inflation_pct"])

# === Sett 'month' som indeks
df.set_index("month", inplace=True)

# === Sørg for at tallene er numeriske
df["inflation_pct"] = pd.to_numeric(df["inflation_pct"], errors="coerce")

# === Lag komplett månedlig indeks med månedsslutt
monthly_index = pd.date_range(start=df.index.min(), end=df.index.max(), freq="M")

# === Reindekser og interpoler
monthly_df = df.reindex(monthly_index).interpolate(method="linear", limit_direction="both")
monthly_df.index.name = "date"

# === Lagre resultat
monthly_df.to_csv("data/kpi_monthly_interpolated.csv")

# === Forhåndsvis
print("Interpolert KPI-data:")
print(monthly_df.head(12))
