import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import os

# === Load dataset ===
df = pd.read_csv("data/model_dataset.csv", parse_dates=["date"])
df.set_index("date", inplace=True)

# === Ensure output folder exists ===
os.makedirs("results", exist_ok=True)

# === Regression 1: Output gap ===
X1 = df[["r", "g"]]
X1 = sm.add_constant(X1)
y1 = df["output_gap_pct"]
model1 = sm.OLS(y1, X1).fit()

# === Regression 2: Inflation surprise ===
X2 = df[["r", "g", "output_gap_pct"]]
X2 = sm.add_constant(X2)
y2 = df["inflation_surprise"]
model2 = sm.OLS(y2, X2).fit()

# === Show summaries ===
print("\n=== OUTPUT GAP REGRESSION ===")
print(model1.summary())

print("\n=== INFLATION SURPRISE REGRESSION ===")
print(model2.summary())

# === Plot fitted vs actual ===
plt.figure(figsize=(12,5))
plt.plot(df.index, y1, label="Actual Output Gap")
plt.plot(df.index, model1.fittedvalues, label="Fitted Output Gap", linestyle="--")
plt.legend(); plt.grid(); plt.title("Output Gap: Actual vs Fitted")
plt.tight_layout(); plt.savefig("results/output_gap_fit.png")
plt.show()

plt.figure(figsize=(12,5))
plt.plot(df.index, y2, label="Actual Inflation Surprise")
plt.plot(df.index, model2.fittedvalues, label="Fitted Inflation Surprise", linestyle="--")
plt.legend(); plt.grid(); plt.title("Inflation Surprise: Actual vs Fitted")
plt.tight_layout(); plt.savefig("results/inflation_surprise_fit.png")
plt.show()

# === Save results ===
coef_df = pd.DataFrame({
    "output_gap": model1.params,
    "inflation_surprise": model2.params
})
coef_df.to_csv("results/estimated_coefficients.csv")

df["output_gap_fitted"] = model1.fittedvalues
df["inflation_surprise_fitted"] = model2.fittedvalues
df.to_csv("results/model_estimates.csv")

print("\n✔️ Regressions complete. Results saved in 'results/' folder.")