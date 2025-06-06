import pandas as pd
import statsmodels.api as sm
import os

# === Load dataset ===
df = pd.read_csv("data/model_dataset.csv", parse_dates=["date"])
df.set_index("date", inplace=True)

# === Compute 12-month average of interest rate ===
df["r_avg12"] = df["r"].rolling(window=12, min_periods=12).mean()
df = df.dropna(subset=["r_avg12"])  # Drop rows with NaNs


# === Ensure output folder exists ===
os.makedirs("results", exist_ok=True)

# === Helper function for regression ===
def run_regression(y_var, x_vars, df, label):
    X = df[x_vars]
    X = sm.add_constant(X)
    y = df[y_var]
    model = sm.OLS(y, X).fit()
    model_hac = model.get_robustcov_results(cov_type='HAC', maxlags=1)
    print(f"\n=== {label.upper()} REGRESSION (Newey-West) ===")
    print(model_hac.summary())
    return model_hac

# === Regressions: Effect of r_avg12 on c, i, nx ===
model_c = run_regression("c", ["r_avg12"], df, "Consumption")
model_i = run_regression("i", ["r_avg12"], df, "Investment")
model_nx = run_regression("nx", ["r_avg12"], df, "Net Exports")

# === Save coefficients ===
coef_df = pd.DataFrame({
    "consumption": model_c.params,
    "investment": model_i.params,
    "net_exports": model_nx.params,
})
coef_df.to_csv("results/r_effect_on_components.csv")

# === Save full stats ===
stats_df = pd.concat([
    model_c.summary2().tables[1].add_prefix("c_"),
    model_i.summary2().tables[1].add_prefix("i_"),
    model_nx.summary2().tables[1].add_prefix("nx_"),
], axis=1)
stats_df.to_csv("results/r_effect_on_components_detailed.csv")

print("\n✔️ Component regressions complete. Results saved in 'results/' folder.")
