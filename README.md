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
- **States:** CA, MA (expensive), FL, TX (mid), MI, OH (low), grouped by state median home value
- **Scope:** first-lien, home-purchase loans for a primary, site-built home
- **Observation unit:** One row is one approved 30-year fixed-rate home-purchase mortgage: it has state, loan type (Conventional, FHA or VA), interest rate, rate spread, total closing costs, loan amount, loan-to-value ratio and borrower income. Four fields were created during cleaning and added to each loan: the state’s home-price tier, a readable loan-type label, a down-payment group (from the loan-to-value ratio) and closing costs as a percentage of the loan.
- **Final app data:** About 2.28 million raw application rows × 99 columns (six states, 2025), filtered to 810,670 approved 30-year fixed-rate loans × 11 columns used in the app.

## Data Access
**To run the app, you don't need to download anything.** The cleaned data (`data/processed/hmda_2025_pricing_clean.parquet`, 17.9 MB) is in the repo, so the app runs straight after cloning. No API key or login is needed.

**To rebuild the data from scratch:**
1. Go to the [CFPB HMDA Data Browser](https://ffiec.cfpb.gov/data-browser/) and choose **Year 2025**, then **State**: CA, MA, FL, TX, MI, OH (one at a time).
2. Filter **Loan purpose = Home purchase** and download the CSV for each state.
3. Save the six files in the project folder as `loan_purposes_1_state_XX.csv` (for example, `loan_purposes_1_state_CA.csv`).
4. In both the notebooks, just set `PROJECT_DIR` to your project folder, then run notebook 1 and then notebook 2.

- The original downloaded files are too big for GitHub, so they aren’t included here.
- Notebook 1 counts the rows in each file. If a count is smaller than the number the HMDA website shows, the download didn’t finish. Download that state again, and delete its old file in data/raw/ before you re-run.
- The data/raw/ and data/interim/ folders aren’t on GitHub either. The notebooks create them for you when you run them.

## Repository contents
| File | What it does |
|---|---|
| `app.py` | Streamlit app |
| `CMSE_HMDA_data_preparation_steps_notebook_1.ipynb` | Loads the raw CSVs, checks row counts, applies scope filters |
| `CMSE_HMDA_project_notebook_2.ipynb` | Cleans approved loans, creates new features, explores both questions |
| `data/processed/hmda_2025_pricing_clean.parquet` | Cleaned data used by the app |
| `data/funnel_scope.csv`, `data/funnel_cleaning.csv` | Number of rows kept at each filtering step |
| `requirements.txt` | Python dependencies|
| `AI_DISCLOSURE.md` | Ai-use disclosure |

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

