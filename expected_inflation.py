import pandas as pd
import matplotlib.pyplot as plt

# Read the file with correct separator
df = pd.read_csv("data/forventet_inflasjon.csv", sep=";", decimal=",")

# Rename columns for clarity
df.columns = ["date", "kpi_now", "kpi_2y_exp", "kpi_5y_exp", "target"]

# Parse date column and set as index
df["date"] = pd.to_datetime(df["date"], format="%d.%m.%Y")
df.set_index("date", inplace=True)

# Convert all other columns to numeric (handles missing values)
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(df.index, df["kpi_now"], label="KPI Now")
plt.plot(df.index, df["kpi_2y_exp"], label="2-Year Expectation")
plt.plot(df.index, df["kpi_5y_exp"], label="5-Year Expectation")
plt.plot(df.index, df["target"], linestyle="--", color="gray", label="Inflation Target")

plt.title("Inflation and Expectations (2002–2024)")
plt.ylabel("Percent")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("data/expected_inflation.png")
plt.show()
