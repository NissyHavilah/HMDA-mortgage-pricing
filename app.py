from pathlib import Path

import pandas as pd
import streamlit as st

# 1. Load the cleaned data saved in notebook 02 (Step 6)
#    Path(__file__).parent = the folder this app.py file is in,
#    so the app finds the data no matter where it's started from.
DATA_FILE = Path(__file__).parent / "data" / "processed" / "hmda_2025_pricing_clean.parquet"
df = pd.read_parquet(DATA_FILE)

# 2. Title and purpose
st.title("What Makes a Mortgage Cost More?")
st.write("Explore what borrowers paid for 30-year fixed-rate home-purchase loans in 2025 "
         "(HMDA data, six states).")

# 3. Let the user choose a state and a loan type
state = st.selectbox("Choose a state", ["CA", "MA", "FL", "TX", "MI", "OH"])
loan_type = st.selectbox("Choose a loan type", ["Conventional", "FHA", "VA"])

# 4. Keep only the loans that match the user's choices
selected = df[(df["state_code"] == state) & (df["loan_type_label"] == loan_type)]
st.write(f"Number of matching loans: {len(selected):,}")

# 5. Median rate spread for each down-payment group
summary = selected.groupby("down_payment_band", observed=True)["rate_spread"].median()

# 6. Show the result as a bar chart
st.subheader("Median rate spread by down payment")
st.bar_chart(summary)
st.caption("Rate spread = how far the loan's APR (interest plus fees and mortgage insurance) "
           "was above the market average, in percentage points.")

# 7. Limitation
st.info("These are past loans, not rate quotes. HMDA does not include credit scores, "
        "which strongly affect the rate a borrower gets.")
