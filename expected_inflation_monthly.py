import pandas as pd
import matplotlib.pyplot as plt

# === Load expected inflation monthly ===
df = pd.read_csv("data/expected_inflation_monthly.csv", parse_dates=["date"])
df.set_index("date", inplace=True)

# DEBUG: Show available columns
print("Columns:", df.columns.tolist())
print(df.head())

# === Plot all in one chart ===
plt.figure(figsize=(12, 6))
plt.plot(df.index, df["kpi_now"], label="KPI nå (rapportert)", color="tab:blue")
plt.plot(df.index, df["kpi_2y_exp"], label="Forventet inflasjon om 2 år", color="tab:orange")
plt.plot(df.index, df["kpi_5y_exp"], label="Forventet inflasjon om 5 år", color="tab:green")
plt.plot(df.index, df["target"], "--", color="gray", label="Inflasjonsmål (2 %)")

plt.title("Konsumprisvekst og forventninger (Interpolert månedlig)")
plt.xlabel("Dato")
plt.ylabel("Prosent")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("data/expected_inflation_monthly_combined.png")
plt.show()


# === Save cleaned dataset (optional) ===
df.to_csv("data/expected_inflation_cleaned.csv")
