import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import os

# === Load dataset ===
df = pd.read_csv("data/model_dataset.csv", parse_dates=["date"])
df.set_index("date", inplace=True)

# === Add 12 monthly lags of interest rate gap (r) ===
for lag in range(1, 13):
    df[f"r_lag{lag}"] = df["r"].shift(lag)

# Drop early rows with NaN from lagging
df = df.dropna()

# === Ensure output folder exists ===
os.makedirs("results", exist_ok=True)

# === Regression 1: Output gap ===
X1_vars = ["r"] + [f"r_lag{lag}" for lag in range(1, 13)] + ["g", "c", "i", "nx"]
X1 = df[X1_vars]
X1 = sm.add_constant(X1)
y1 = df["output_gap_pct"]
model1 = sm.OLS(y1, X1).fit()
model1_hac = model1.get_robustcov_results(cov_type='HAC', maxlags=1)

# === Regression 2: Inflation surprise ===
X2_vars = ["r"] + [f"r_lag{lag}" for lag in range(1, 13)] + ["g", "c", "i", "nx", "output_gap_pct"]
X2 = df[X2_vars]
X2 = sm.add_constant(X2)
y2 = df["inflation_surprise"]
model2 = sm.OLS(y2, X2).fit()
model2_hac = model2.get_robustcov_results(cov_type='HAC', maxlags=1)

# === Show summaries ===
print("\n=== OUTPUT GAP REGRESSION (Newey-West) ===")
print(model1_hac.summary())

print("\n=== INFLATION SURPRISE REGRESSION (Newey-West) ===")
print(model2_hac.summary())

# === Plot fitted vs actual ===
plt.figure(figsize=(12, 5))
plt.plot(df.index, y1, label="Actual Output Gap")
plt.plot(df.index, model1_hac.fittedvalues, label="Fitted Output Gap", linestyle="--")
plt.legend()
plt.grid()
plt.title("Output Gap: Actual vs Fitted")
plt.tight_layout()
plt.savefig("results/output_gap_fit.png")
plt.show()

plt.figure(figsize=(12, 5))
plt.plot(df.index, y2, label="Actual Inflation Surprise")
plt.plot(df.index, model2_hac.fittedvalues, label="Fitted Inflation Surprise", linestyle="--")
plt.legend()
plt.grid()
plt.title("Inflation Surprise: Actual vs Fitted")
plt.tight_layout()
plt.savefig("results/inflation_surprise_fit.png")
plt.show()

# === Save coefficients ===
coef1 = pd.Series(model1_hac.params, name="output_gap")
coef2 = pd.Series(model2_hac.params, name="inflation_surprise")
coef_df = pd.concat([coef1, coef2], axis=1)
coef_df.to_csv("results/estimated_coefficients.csv")

# === Save detailed stats (matching by index) ===
stats1 = pd.DataFrame({
    "coef_output_gap": model1_hac.params,
    "se_output_gap": model1_hac.bse,
    "pval_output_gap": model1_hac.pvalues,
})
stats2 = pd.DataFrame({
    "coef_infl_surprise": model2_hac.params,
    "se_infl_surprise": model2_hac.bse,
    "pval_infl_surprise": model2_hac.pvalues,
})
stats_df = stats1.join(stats2, how="outer")
stats_df.to_csv("results/estimated_coefficients_detailed.csv")

# === Save fitted values ===
df["output_gap_fitted"] = model1_hac.fittedvalues
df["inflation_surprise_fitted"] = model2_hac.fittedvalues
df.to_csv("results/model_estimates.csv")

print("\n✔️ Regressions complete. Results saved in 'results/' folder.")
