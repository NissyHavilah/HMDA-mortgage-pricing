# What Makes a Mortgage Cost More?

An interactive Streamlit app that shows homebuyers what borrowers like them paid for a
30-year fixed-rate home-purchase mortgage in 2025, and how down payment, loan type and
state relate to the price.

## Data
- **Source:** Home Mortgage Disclosure Act (HMDA) loan-level data, 2025, from the
  [CFPB HMDA Data Browser](https://ffiec.cfpb.gov/data-browser/)
- **Observation unit:** one mortgage application
- **States:** two per home-price tier (Zillow median home value, July 2025):
  California and Massachusetts (expensive), Florida and Texas (mid), Michigan and Ohio (low)

| Stage | Loans |
|---|---|
| Downloaded (6 states, home purchase) | 2,282,462 |
| In scope (first lien, primary home, site-built, consumer loan) | 1,747,609 |
| Originated (approved and made) | 970,201 |
| Cleaned (30-year fixed rate, valid values) | 810,670 |

Data files are not stored in this repository because of their size.

## How to reproduce
1. Download each state from the Data Browser: *Dataset by State* → 2025 → state →
   *Loan Purpose: Home purchase*. Save the six CSV files in the project folder.
2. Install packages: `pip install -r requirements.txt`
3. Run `CMSE_HMDA_data_preparation_steps_notebook_1.ipynb` (download checks and scope filters).
4. Run `CMSE_HMDA_project_notebook_2.ipynb` (cleaning, analysis, saves the app data).
5. Start the app: `streamlit run app.py`

Update `PROJECT_DIR` at the top of each notebook to your own folder path.

## Key limitations
- HMDA does not include credit scores, which strongly affect mortgage pricing.
- Figures describe past loans; they are not rate quotes.
- Patterns are associations, not causes.
- Small lenders are exempt from reporting some fields (about 1.4% of loans).

## AI use
**Tool:** Claude (Anthropic), Claude Opus 5.5 used throughout the project.

- **Purpose(s) or representative prompt(s):**
- Project exploration: Compared potential datasets, including HMDA, the Survey of Consumer Finances, SEC Financial Statement Data Sets, and SEDA.
- State selection: Explored ways to select states representing different home-price levels for mortgage-pricing comparisons.
- Coding and debugging: Received assistance with loading and filtering HMDA data in pandas, resolving coding errors, and organizing Streamlit components, including sidebar inputs, user-entered values, and charts.
- Documentation: Received assistance with drafting Markdown explanations and code comments.


- **How you checked the output:**
- Executed the suggested code myself and verified results against the raw HMDA data, including row counts by state, rate-spread and interest-rate ranges, and missing-value counts before and after cleaning.
- Verified HMDA field definitions using the official CFPB HMDA data documentation: https://ffiec.cfpb.gov/documentation/publications/loan-level-datasets/lar-data-fields/#lei
- Tested the Streamlit application with different user inputs and checked whether the displayed results updated correctly and were reasonable

- **Your own analytical contribution / decisions:**
- Selected the HMDA mortgage dataset (it took forever to find the one I was looking for) and came up with the project question: Who pays more for a mortgage, and how does mortgage pricing vary across borrower and loan characteristics?
- Selected six states (CA, MA, FL, TX, MI, and OH), with two representing each of the three home-price tiers, to compare mortgage pricing across different housing markets.
- Defined the midterm project's scope around mortgage pricing, while reserving lender-level variation and the approval/denial prediction task for the final project.
- Made the data-cleaning decisions and determined which variables and records to include in the analysis.
- Selected the visualizations and designed the Streamlit interface to let users enter borrower and loan characteristics and explore the resulting pricing information.
- Interpreted the findings and developed the conclusions myself, drawing on my prior experience with mortgage credit-risk modeling.
- AI assistance supported implementation, debugging, and documentation. I remained responsible for the project's analytical decisions, validation, interpretation, and conclusions.
