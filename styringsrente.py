import pandas as pd

# Last inn data
df = pd.read_csv("data/IR.csv", sep=";", encoding="utf-8")

# Rens kolonnenavn
df.columns = df.columns.str.strip().str.lower()

# Filtrer etter styringsrenten
mask = (
    (df["instrument_type"] == "KPRA") &
    (df["instrumenttype"] == "Styringsrenten")
)
df = df[mask].copy()

# Konverter dato og verdi
df["date"] = pd.to_datetime(df["time_period"], format="%Y-%m-%d", errors="coerce")
df["obs_value"] = pd.to_numeric(df["obs_value"].str.replace(",", "."), errors="coerce")

# Lag månedlig gjennomsnitt
monthly_df = (
    df.set_index("date")
    .resample("M")["obs_value"]
    .mean()
    .rename("policy_rate")
    .to_frame()
)

# Lagre resultatet
monthly_df.to_csv("data/policy_rate_cleaned.csv")

print(monthly_df.head())
