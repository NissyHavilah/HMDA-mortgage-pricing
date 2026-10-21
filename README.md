# What Makes a Mortgage Cost More?

**Live app:** https://hmda-mortgage-pricing.streamlit.app/

A Streamlit app that helps first-time home buyers see what borrowers like them actually paid for a mortgage, based on their down payment, loan type and the state where they want to buy their home.

## Project purpose
Buying a first home is one of the very important and biggest financial decision people make, but it is hard to know and understand how the mortgage price looks like. This app uses Home Mortgage Disclosure Act (HMDA) data for the year 2025 to show what other borrowers actually paid. By using this app a user can see how different factors like down payment, loan type and state relate to the mortgage price. This app was especially built for people who are interested to buy their first home and ready to pay a 30-year fixed rate mortgage.

**Who it's for:** people planning to buy their first home, and anyone curious about how mortgage prices vary.

## Primary question
**How do a borrower's down payment, loan type and state relate to what they pay for a 30-year fixed-rate home-purchase mortgage?**

Supporting questions:
1. **Down payment:** Does a smaller down payment mean a higher price (rate spread), and does this differ for Conventional, FHA and VA loans?
2. **Closing costs:** Do closing costs differ across states, in dollars and as a share of the loan?

## What the app does
The app has six tabs:
- **Home:** what the app is for, how to use it, and what the key words mean.(rate spread, down payment, loan types).
- **Borrowers like you:** Pick a state (U.S state), loan type and down payment and see what people like you paid.
- **Down payment:** a chart of median rate spread by down payment for each loan type, filterable by state.
- **Closing costs:** compare the fees people paid in each of the six states.
- **Data & preparation:** the data source, how many loans were kept at each cleaning step, and the key decisions.
- **Limitations:** what the data can and can't tell you.
  
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

