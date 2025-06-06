import pandas as pd
import matplotlib.pyplot as plt

# === Load directly from SSB export ===
URL = "http://www.ssb.no/statbank/sq/10111990"  # <- Your latest valid semicolon-separated export

# === Load raw data
df_raw = pd.read_csv(URL, sep=';', encoding='latin1', skiprows=2)

# === Velg bare tallrekken (rad 0, uten første kolonne)
kpi_row = df_raw.iloc[0, 1:]
months = df_raw.columns[1:]

# === Lag DataFrame i langformat ===
df = pd.DataFrame({
    "month_str": months,
    "kpi": kpi_row.values
})

# === Rens KPI-verdier ===
df["kpi"] = (
    df["kpi"]
    .astype(str)
    .str.replace(r"\s+", "", regex=True)
    .str.replace(",", ".", regex=False)
)
df["kpi"] = pd.to_numeric(df["kpi"], errors="coerce")

# === Norsk månedskart
norsk_maaned_map = {
    "januar": 1, "februar": 2, "mars": 3, "april": 4,
    "mai": 5, "juni": 6, "juli": 7, "august": 8,
    "september": 9, "oktober": 10, "november": 11, "desember": 12
}

def parse_norsk_month(s):
    try:
        år, mnd = s.strip().split()
        mnd_num = norsk_maaned_map[mnd.lower()]
        return pd.Timestamp(year=int(år), month=mnd_num, day=1)
    except Exception:
        return pd.NaT

# === Bruk egendefinert parser
df["month"] = df["month_str"].apply(parse_norsk_month)
df.dropna(subset=["month", "kpi"], inplace=True)
df = df[["month", "kpi"]].sort_values("month")
df.set_index("month", inplace=True)

# === Årsendring i KPI
df["inflation_pct"] = df["kpi"].pct_change(12) * 100

# === Plott KPI
plt.figure(figsize=(12, 6))
plt.plot(df.index, df["kpi"], label="KPI (2015=100)")
plt.title("Konsumprisindeks (2015=100)")
plt.xlabel("Dato")
plt.ylabel("Indeksverdi")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("data/kpi_index.png")
plt.show()

# === Plott inflasjon
plt.figure(figsize=(12, 6))
plt.plot(df.index, df["inflation_pct"], label="Inflasjon (år/år)", color="orange")
plt.axhline(0, color="black", linestyle="--", linewidth=1)
plt.title("Årsvekst i KPI (Inflasjon)")
plt.xlabel("Dato")
plt.ylabel("Prosent")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("data/kpi_inflation_pct.png")
plt.show()

# === Lagre data
df.to_csv("data/kpi_cleaned.csv")
