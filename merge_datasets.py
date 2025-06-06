import pandas as pd

# === Load datasets ===
df_y = pd.read_csv("data/output_gap_monthly.csv", parse_dates=["month"])
df_pi = pd.read_csv("data/kpi_cleaned.csv", parse_dates=["month"])
df_pi_exp = pd.read_csv("data/expected_inflation_cleaned.csv", parse_dates=["date"])
df_r = pd.read_csv("data/real_interest_rate_gap.csv", parse_dates=["date"])
df_g = pd.read_csv("data/gov_demand_gap.csv", parse_dates=["month"])
df_c = pd.read_csv("data/gap_consumption.csv", parse_dates=["month"])
df_i = pd.read_csv("data/gap_investment.csv", parse_dates=["month"])
df_nx = pd.read_csv("data/gap_net_export.csv", parse_dates=["month"])

# === Standardize dates to month-end ===
df_y["date"] = df_y["month"] + pd.offsets.MonthEnd(0)
df_pi["date"] = df_pi["month"] + pd.offsets.MonthEnd(0)
df_g["date"] = df_g["month"] + pd.offsets.MonthEnd(0)
df_c["date"] = df_c["month"] + pd.offsets.MonthEnd(0)
df_i["date"] = df_i["month"] + pd.offsets.MonthEnd(0)
df_nx["date"] = df_nx["month"] + pd.offsets.MonthEnd(0)

# === Interpolate inflation BEFORE merge ===
# Ensure a complete monthly index
date_range = pd.date_range(start=df_y["date"].min(), end=df_y["date"].max(), freq="M")
df_pi = df_pi.set_index("date").reindex(date_range)
df_pi["inflation_pct"] = df_pi["inflation_pct"].interpolate(method="linear")
df_pi = df_pi.reset_index().rename(columns={"index": "date"})

# === Select and rename columns ===
df_y = df_y[["date", "output_gap_pct"]]
df_pi = df_pi[["date", "inflation_pct"]]
df_pi_exp = df_pi_exp[["date", "kpi_2y_exp"]].rename(columns={"kpi_2y_exp": "inflation_expected"})
df_r = df_r[["date", "r_gap"]].rename(columns={"r_gap": "r"})
df_g = df_g[["date", "g_gap_pct"]].rename(columns={"g_gap_pct": "g"})
df_c = df_c[["date", "c_gap_pct"]].rename(columns={"c_gap_pct": "c"})
df_i = df_i[["date", "i_gap_pct"]].rename(columns={"i_gap_pct": "i"})
df_nx = df_nx[["date", "nx_gap_pct"]].rename(columns={"nx_gap_pct": "nx"})

# === Merge all on date ===
dfs = [df_y, df_pi, df_pi_exp, df_r, df_g, df_c, df_i, df_nx]
df_model = dfs[0]
for df in dfs[1:]:
    df_model = df_model.merge(df, on="date", how="inner")

# === Compute inflation surprise ===
df_model["inflation_surprise"] = df_model["inflation_pct"] - df_model["inflation_expected"]

# === Preview and save ===
print("\nMerged dataset:")
print(df_model.head())
print("\nFinal shape:", df_model.shape)

df_model.to_csv("data/model_dataset.csv", index=False)

