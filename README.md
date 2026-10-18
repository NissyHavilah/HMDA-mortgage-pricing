# What Makes a Mortgage Cost More?

**Live app:** https://hmda-mortgage-pricing.streamlit.app/

A Streamlit data story for CMSE 830 (Fall 2026) using 2025 HMDA mortgage data from six US states.

## Project purpose
Buying a home is one of the biggest financial decisions people make, but it is hard to know what a "normal" mortgage price looks like. This app uses public 2025 loan records to show what borrowers actually paid, so home buyers can see how their down payment, loan type and state relate to the price of a 30-year fixed-rate mortgage.

**Who it's for:** people planning to buy a home, and anyone curious about how mortgage prices vary.

## Questions
1. Does a smaller down payment mean a higher price (rate spread), and does it differ by loan type (Conventional, FHA, VA)?
2. Do closing costs differ across states, in dollars and as a share of the loan?

## Data
- **Source:** Home Mortgage Disclosure Act (HMDA) 2025 loan-level data,
- [CFPB HMDA Data Browser](https://ffiec.cfpb.gov/data-browser/)
- **States:** CA, MA (expensive), FL, TX (mid), MI, OH (low)
- **Scope:** first-lien, home-purchase loans for a primary, site-built home
- **Final app data:** 810,670 approved 30-year fixed-rate loans

## Repository contents
| File | What it does |
|---|---|
| `CMSE_HMDA_data_preparation_steps_notebook_1.ipynb` | Loads raw CSVs, checks row counts, applies scope filters |
| `CMSE_HMDA_project_notebook_2.ipynb` | Cleans approved loans, creates features, EDA for both questions |
| `app.py` | Streamlit app |
| `data/processed/hmda_2025_pricing_clean.parquet` | Cleaned data used by the app |
| `data/funnel_scope.csv`, `data/funnel_cleaning.csv` | Row counts at each filtering step |

Raw and interim data are not in the repo because they are too large.

## How to run the app locally
```
pip install -r requirements.txt
streamlit run app.py
```

## How to reproduce the data
   1. Go to the [HMDA Data Browser](https://ffiec.cfpb.gov/data-browser/) and choose Year 2025, then each state (CA, MA, FL, TX, MI, OH).
   2. Filter: Loan purpose = Home purchase. Download the CSV for each state.
   3. Save the files in the project folder as `loan_purposes_1_state_XX.csv`.
   4. In both notebooks, set `PROJECT_DIR` to your project folder.
   5. Run notebook 1, then notebook 2.

## Limitations
- No credit scores in HMDA, which strongly affect rates
- Associations, not causes
- Past loans, not rate quotes
- Six states only

