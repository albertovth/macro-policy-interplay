import pandas as pd
import os

# === Paths ===
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# === Load dataset ===
df = pd.read_csv(f"{DATA_DIR}/model_dataset.csv", parse_dates=["date"])
df.set_index("date", inplace=True)

# === Select relevant variables ===
df_final = df[[
    "output_gap_pct",
    "inflation_pct",
    "exp_inflation",   # this is 2-year expected inflation
    "r",               # real interest rate
    "g",               # fiscal gap
    "inflation_surprise"
]].copy()

# Optional: rename for clarity or backward compatibility
df_final.rename(columns={"exp_inflation": "kpi_2y_exp"}, inplace=True)

# === Save final model dataset ===
df_final.reset_index().to_csv(f"{DATA_DIR}/final_model_data.csv", index=False)
print("✅ Saved final dataset to data/final_model_data.csv")

