import matplotlib.pyplot as plt
import pandas as pd




# Load results
df = pd.read_csv("data/final_model_data.csv", parse_dates=["date"])
df["fitted_output_gap"] = (
    -0.1397
    + 0.0685 * df["r"]
    + 0.3462 * df["g"]
)

plt.figure(figsize=(12, 6))
plt.plot(df["date"], df["output_gap_pct"], label="Observed Output Gap", color="tab:blue")
plt.plot(df["date"], df["fitted_output_gap"], label="Fitted Output Gap", color="tab:orange", linestyle="--")
plt.axhline(0, color="gray", linestyle=":")
plt.title("Output Gap: Observed vs Fitted")
plt.xlabel("Date")
plt.ylabel("Percent")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("data/output_gap_fit_vs_actual.png")
plt.show()
