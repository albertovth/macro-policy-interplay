import pandas as pd
import statsmodels.api as sm
import os
import matplotlib.pyplot as plt

# === Load dataset ===
df = pd.read_csv("data/model_dataset.csv", parse_dates=["date"])
df.set_index("date", inplace=True)

# === Create lagged predictors ===
df["g_lag1"] = df["g"].shift(1)
df["c_lag1"] = df["c"].shift(1)
df["i_lag1"] = df["i"].shift(1)
df["nx_lag1"] = df["nx"].shift(1)

# === Drop missing due to lagging ===
df_reg = df[["r", "g_lag1", "c_lag1", "i_lag1", "nx_lag1"]].dropna()

# === Regression: r ~ lagged g, c, i, nx ===
X = df_reg[["g_lag1", "c_lag1", "i_lag1", "nx_lag1"]]
X = sm.add_constant(X)
y = df_reg["r"]

model = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": 1})

# === Print summary ===
print("\n=== INTEREST RATE REGRESSION ON LAGGED DEMAND COMPONENTS (Newey-West) ===")
print(model.summary())

# === Plot fitted vs actual ===
os.makedirs("results", exist_ok=True)

plt.figure(figsize=(12, 5))
plt.plot(df_reg.index, y, label="Actual r")
plt.plot(df_reg.index, model.fittedvalues, linestyle="--", label="Fitted r")
plt.title("Real Interest Rate: Actual vs Fitted")
plt.grid()
plt.legend()
plt.tight_layout()
plt.savefig("results/interest_rate_response_fit.png")
plt.show()

# === Save coefficients and fitted values ===
model.params.to_csv("results/interest_rate_response_coefficients.csv")
df_reg["r_fitted"] = model.fittedvalues
df_reg[["r", "r_fitted"]].to_csv("results/interest_rate_response_values.csv")

print("\n✔️ Regression complete. Results saved in 'results/' folder.")
