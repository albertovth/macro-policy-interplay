import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import os

# === Load dataset ===
df = pd.read_csv("data/model_dataset.csv", parse_dates=["date"])
df.set_index("date", inplace=True)

# === Ensure output folder exists ===
os.makedirs("results", exist_ok=True)

# === Add lagged variables (optional extension) ===
df["output_gap_lag1"] = df["output_gap_pct"].shift(1)
df["inflation_surprise_lag1"] = df["inflation_surprise"].shift(1)

# Drop rows with missing lags (first row usually)
df.dropna(inplace=True)

# === Regression 1: Output gap ===
X1 = df[["r", "g", "output_gap_lag1"]]  # Include lag of output gap
X1 = sm.add_constant(X1)
y1 = df["output_gap_pct"]
model1 = sm.OLS(y1, X1).fit()

# === Regression 2: Inflation surprise ===
X2 = df[["r", "g", "output_gap_pct", "inflation_surprise_lag1"]]  # Include lag
X2 = sm.add_constant(X2)
y2 = df["inflation_surprise"]
model2 = sm.OLS(y2, X2).fit()

# === Show summaries ===
print("\n=== OUTPUT GAP REGRESSION (Extended) ===")
print(model1.summary())

print("\n=== INFLATION SURPRISE REGRESSION (Extended) ===")
print(model2.summary())

# === Plot fitted vs actual ===
plt.figure(figsize=(12, 5))
plt.plot(df.index, y1, label="Actual Output Gap")
plt.plot(df.index, model1.fittedvalues, label="Fitted Output Gap", linestyle="--")
plt.legend(); plt.grid(); plt.title("Output Gap: Actual vs Fitted (Extended)")
plt.tight_layout(); plt.savefig("results/output_gap_fit_extended.png")
plt.show()

plt.figure(figsize=(12, 5))
plt.plot(df.index, y2, label="Actual Inflation Surprise")
plt.plot(df.index, model2.fittedvalues, label="Fitted Inflation Surprise", linestyle="--")
plt.legend(); plt.grid(); plt.title("Inflation Surprise: Actual vs Fitted (Extended)")
plt.tight_layout(); plt.savefig("results/inflation_surprise_fit_extended.png")
plt.show()

# === Save results ===
coef_df = pd.DataFrame({
    "output_gap": model1.params,
    "inflation_surprise": model2.params
})
coef_df.to_csv("results/estimated_coefficients_extended.csv")

# Save extended dataset with fitted values
fitted_df = df.copy()
fitted_df["output_gap_fitted"] = model1.fittedvalues
fitted_df["inflation_surprise_fitted"] = model2.fittedvalues
fitted_df.to_csv("results/model_estimates_extended.csv")

print("\n✔️ Extended regressions complete. Results saved in 'results/' folder.")
