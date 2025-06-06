import pandas as pd
import matplotlib.pyplot as plt

# Last inn styringsrente (start-of-month, flyttet til månedsslutt)
policy = pd.read_csv("data/policy_rate_cleaned.csv", parse_dates=["date"])
policy["date"] = policy["date"] + pd.offsets.MonthEnd(0)
policy.set_index("date", inplace=True)

# Last inn forventet inflasjon (allerede på månedsslutt)
infl = pd.read_csv("data/expected_inflation_cleaned.csv", parse_dates=["date"])
infl.set_index("date", inplace=True)

# Merge på månedsslutt
df = policy.join(infl, how="inner")

# Bruk 2-årig forventet inflasjon (juster ved behov)
df["exp_inflation"] = df["kpi_2y_exp"]

# Beregn realrente
df["r_real"] = df["policy_rate"] - df["exp_inflation"]

# Antatt nøytral realrente
r_neutral = 1.0
df["r_gap"] = df["r_real"] - r_neutral

# Lagre og visualiser
df[["policy_rate", "exp_inflation", "r_real", "r_gap"]].to_csv("data/real_interest_rate_gap.csv")

plt.figure(figsize=(12, 6))
plt.plot(df.index, df["r_gap"], label="Reell rentegap", color="tab:red")
plt.axhline(0, linestyle="--", color="gray")
plt.title("Reell rentegap (styringsrente – forventet inflasjon – nøytral rente)")
plt.ylabel("Prosent")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("data/real_interest_rate_gap_plot.png")
plt.show()
