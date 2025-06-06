import pandas as pd
import statsmodels.api as sm

# === Load dataset ===
df = pd.read_csv("data/model_dataset.csv", parse_dates=["date"])
df.set_index("date", inplace=True)

# === Define regression function ===
def run_regression(dep_var, indep_var):
    X = df[indep_var]
    X = sm.add_constant(X)
    y = df[dep_var]
    model = sm.OLS(y, X).fit()
    model_hac = model.get_robustcov_results(cov_type='HAC', maxlags=1)
    print(f"\n=== {dep_var.upper()} REGRESSION (Newey-West) ===")
    print(model_hac.summary())

# === Run regressions with raw r ===
run_regression("c", ["r"])
run_regression("i", ["r"])
run_regression("nx", ["r"])
