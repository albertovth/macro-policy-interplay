# Macro Policy Interplay

This project explores the interaction between monetary and fiscal policy in a small open economy — particularly under conditions where the traditional monetary transmission mechanism is impaired.

## Purpose

The goal is to understand:

- How fiscal policy (government demand) and monetary policy (interest rates) jointly influence the **output gap** and **inflation**.
- Whether fiscal expansion can offset contractionary monetary policy, especially when private demand components (consumption, investment, net exports) are **insensitive** to interest rate changes.
- Whether this situation resembles a **rich-country liquidity trap** where real interest rates have limited traction on economic activity.

## Methods

- Based on empirical models inspired by the Norges Bank Staff Memo 16/2023 The interplay between monetary and fiscal policy in a small open economy
- Uses monthly time series data since 2016 from official sources (SSB, Norges Bank).
- Core regressions estimate the impact of:
  - Real interest rate (12-month average)
  - Government demand gap
  - Consumption, investment, and net exports
  - On both **output gap** and **inflation surprise**

- Regression models are estimated using OLS with **Newey-West (HAC)** standard errors.

## Main Results

- **Output gap** is significantly driven by **government demand**, **consumption**, and **investment**, but **not strongly by interest rates**.
- **Inflation** is significantly affected by **interest rates**, the **output gap**, and **government demand**, supporting the view that:
  - High interest rates reduce inflation (possibly via exchange rate effects),
  - Fiscal expansion can sustain output without significantly fueling inflation.

This supports the hypothesis that a **strategic mix of high interest rates and fiscal expansion** may be optimal in certain contexts — especially when inflation is externally driven and monetary policy has weak domestic traction. This presents challenges for long-term sustainability and the expansion of the private sector.

## Structure

macro-policy-interplay/  
├── data/  
│   ├── model_dataset.csv            # Final dataset used for regression  
│   └── ...                          # Other source/intermediate files  
├── results/  
│   ├── model_estimates.csv          # Fitted values and residuals  
│   ├── estimated_coefficients.csv   # Regression coefficients  
│   └── *.png                        # Plots of fit results  
│   └── *...                         # Other results
├── estimate_models.py               # Main regression logic  
├── estimate_r_on_c_i_g_nx.py        # Secondary regressions: C, I, NX on interest  
├── analyze_correlations.py          # Code for correlation analysis  
└── README.md                        # This file
└──...                               # Other files
## 🔧 Requirements

- Python 3.9+
- Dependencies (install via `pip install -r requirements.txt`):
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `statsmodels`

## License

MIT License (or adapt as needed).
