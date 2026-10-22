from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------
# Settings
# ---------------------------------------------------------------
st.set_page_config(page_title="What Makes a Mortgage Cost More?", layout="wide")

DATA_DIR = Path(__file__).parent / "data"   
STATES = ["CA", "MA", "FL", "TX", "MI", "OH"]
STATE_NAMES = {"CA": "California", "MA": "Massachusetts", "FL": "Florida",
               "TX": "Texas", "MI": "Michigan", "OH": "Ohio"}
STATE_TIERS = {"CA": "Expensive", "MA": "Expensive", "FL": "Mid",
               "TX": "Mid", "MI": "Low", "OH": "Low"}
LOAN_TYPES = ["Conventional", "FHA", "VA"]
DOWN_PAYMENTS = ["20%+ down", "10-20% down", "5-10% down", "3-5% down", "Under 3% down"]
COLORS = ["#0072B2", "#E69F00", "#009E73"]   # I used color-blind-safe colors
MIN_LOANS = 30                               


# ---------------------------------------------------------------
# Load data (cached, so it loads only once)
# ---------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_parquet(DATA_DIR / "processed" / "hmda_2025_pricing_clean.parquet")
    df["down_payment_band"] = df["down_payment_band"].astype(str)
    return df

df = load_data()


# ---------------------------------------------------------------
# Title and tabs
# ---------------------------------------------------------------
st.title("🏠 What Makes a Mortgage Cost More?")
st.write("Explore what borrowers actually paid for a 30-year fixed-rate home-purchase mortgage "
         "in 2025, using public loan records from six US states.")

tab_home, tab_you, tab_q1, tab_q2, tab_data, tab_limits = st.tabs(
    ["Home", "Borrowers like you", "Down payment", "Closing costs", "Data & preparation", "Limitations"])


# ---------------------------------------------------------------
# Tab 1: Home
# ---------------------------------------------------------------
with tab_home:
    st.header("Who is this for?")
    st.write("People planning to buy a home who want to know how their **down payment**, **loan type** "
             "and **location** relate to the price of a mortgage.")

    st.header("How to use this app")
    st.markdown(
        "1. **Borrowers like you:** enter your situation and see what similar borrowers paid.\n"
        "2. **Down payment:** see how the price changes as the down payment gets smaller.\n"
        "3. **Closing costs:** compare fees across states, in dollars and as a share of the loan.\n"
        "4. **Data & preparation** and **Limitations:** how the data was prepared and what it can't tell you.")

    st.header("The data at a glance")
    col1, col2, col3 = st.columns(3)
    col1.metric("Loans analysed", f"{len(df):,}")
    col2.metric("States", "6")
    col3.metric("Year", "2025")
    st.write("States were chosen two per home-price tier: **expensive** (California, Massachusetts), "
             "**mid** (Florida, Texas) and **low** (Michigan, Ohio).")

    st.header("Key terms")
    st.markdown(
        "- **Rate spread:** how far a loan's APR (interest plus fees and mortgage insurance) was above "
        "the market average that week. Higher means the borrower paid more.\n"
        "- **Down payment:** the share of the home price paid upfront. 20% down means a loan of 80% of the price.\n"
        "- **Closing costs:** fees paid to get the loan (lender fees, title insurance and others).\n"
        "- **Loan types:** *Conventional* (standard loan), *FHA* (government-insured, low down payment), "
        "*VA* (for veterans, often no down payment).")

    # ---------------------------------------------------------------
# Tab 2: Borrowers like you
# ---------------------------------------------------------------
with tab_you:
    st.header("What did borrowers like you pay?", anchor=False)
    st.write("Choose your situation. The app finds past loans that match and shows what those borrowers paid.")

    # Three dropdowns side by side
    col1, col2, col3 = st.columns(3)
    state = col1.selectbox("State", STATES, format_func=lambda s: STATE_NAMES[s], key="you_state")
    loan_type = col2.selectbox("Loan type", LOAN_TYPES, key="you_type")
    down_payment = col3.selectbox("Down payment", DOWN_PAYMENTS, key="you_down")

    # Keep only the loans that match all three choices
    match = df[(df["state_code"] == state) &
               (df["loan_type_label"] == loan_type) &
               (df["down_payment_band"] == down_payment)]

    # Too few loans: show a warning instead of unreliable numbers
    if len(match) < MIN_LOANS:
        st.warning(f"Only {len(match)} loans match this combination, which is too few for reliable "
                   "results. Try a different down payment or loan type.")
    else:
        col1, col2, col3 = st.columns(3)
        col1.metric("Typical interest rate", f"{match['interest_rate'].median():.2f}%")
        col2.metric("Typical rate spread", f"{match['rate_spread'].median():+.2f} points")
        col3.metric("Typical closing costs", f"${match['total_loan_costs'].median():,.0f}")
        st.caption(f"Medians of {len(match):,} matching loans. Half of these borrowers had an interest rate "
                   f"between {match['interest_rate'].quantile(0.25):.2f}% and "
                   f"{match['interest_rate'].quantile(0.75):.2f}%.")

    st.info("These are past loans, not a rate quote. Your actual rate also depends on your credit score, "
            "which this data does not include.")


    
    # ---------------------------------------------------------------
# Tab 3: Down payment (Question 1)
# ---------------------------------------------------------------
with tab_q1:
    st.header("Does a smaller down payment mean a higher price?", anchor=False)
    st.write("The chart shows the **median rate spread** for each down-payment group, by loan type. "
             "Choose a state, or look at all six together.")

    state_choice = st.selectbox("State", ["All states"] + STATES,
                                format_func=lambda s: s if s == "All states" else STATE_NAMES[s],
                                key="q1_state")

    # Keep the three main loan types, and the chosen state (if one is chosen)
    q1 = df[df["loan_type_label"].isin(LOAN_TYPES)]
    if state_choice != "All states":
        q1 = q1[q1["state_code"] == state_choice]

    # Median rate spread and number of loans for each down-payment group and loan type
    medians = q1.pivot_table(index="down_payment_band", columns="loan_type_label",
                             values="rate_spread", aggfunc="median")
    counts = q1.pivot_table(index="down_payment_band", columns="loan_type_label",
                            values="rate_spread", aggfunc="count")
    medians = medians.reindex(DOWN_PAYMENTS)          # put groups in order
    counts = counts.reindex(DOWN_PAYMENTS)
    medians = medians.where(counts >= MIN_LOANS)      # hide very small groups

    # Line chart: one line per loan type
    fig, ax = plt.subplots(figsize=(8, 4))
    for loan, color in zip(LOAN_TYPES, COLORS):
        if loan in medians.columns:
            ax.plot(DOWN_PAYMENTS, medians[loan], marker="o", label=loan, color=color)
    ax.axhline(0, color="grey", linestyle="--", linewidth=0.8)
    ax.set_xlabel("Down payment")
    ax.set_ylabel("Median rate spread (points above market)")
    ax.legend(title="Loan type")
    st.pyplot(fig)

    st.markdown(
        "**What it shows:** for **conventional** loans, the price rises as the down payment shrinks, "
        "consistent with mortgage insurance, which is required below 20% down. **FHA** stays fairly flat until "
        "under 3% down. **VA** loans are priced below the market rate at every down payment.")
    st.caption("The dashed line at 0 means 'priced exactly at the market average'. "
               f"Groups with fewer than {MIN_LOANS} loans are hidden.")


    # ---------------------------------------------------------------
# Tab 4: Closing costs (Question 2)
# ---------------------------------------------------------------
with tab_q2:
    st.header("Do closing costs differ across states?", anchor=False)
    st.write("Compare closing costs in **dollars** and as a **share of the loan**. "
             "States are ordered from expensive to low-cost housing markets.")

    loan_choice = st.selectbox("Loan type", ["All loan types"] + LOAN_TYPES, key="q2_type")

    # Keep loans with closing costs; drop costs above 20% of the loan (likely errors)
    q2 = df.dropna(subset=["total_loan_costs"])
    q2 = q2[q2["loan_costs_pct"] <= 20]
    if loan_choice != "All loan types":
        q2 = q2[q2["loan_type_label"] == loan_choice]

    # Median closing costs per state
    summary = q2.groupby("state_code").agg(
        loans=("total_loan_costs", "count"),
        median_cost=("total_loan_costs", "median"),
        median_cost_pct=("loan_costs_pct", "median"),
    ).reindex(STATES)

    # Two bar charts side by side: dollars and % of loan
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    axes[0].bar(STATES, summary["median_cost"], color="#0072B2")
    axes[0].set_title("Median closing costs ($)")
    axes[0].set_ylabel("Dollars")
    axes[1].bar(STATES, summary["median_cost_pct"], color="#E69F00")
    axes[1].set_title("Median closing costs (% of loan)")
    axes[1].set_ylabel("Percent of loan")
    st.pyplot(fig)

    # Table with full state names and tiers
    table = summary.copy()
    table.index = [f"{STATE_NAMES[s]} ({STATE_TIERS[s]})" for s in table.index]
    table.columns = ["Loans", "Median cost ($)", "Median cost (% of loan)"]
    st.dataframe(table.round(2))

    st.markdown(
        "**What it shows:** in dollars, costs roughly follow home prices (highest in California). "
        "As a share of the loan, Texas and Florida pay the most and Massachusetts the least, "
        "so closing costs do not simply follow home prices.")


    # ---------------------------------------------------------------
# Tab 5: Data & preparation
# ---------------------------------------------------------------
with tab_data:
    st.header("Where the data comes from", anchor=False)
    st.markdown(
        "- **Source:** Home Mortgage Disclosure Act (HMDA) loan-level data, 2025, from the "
        "[CFPB HMDA Data Browser](https://ffiec.cfpb.gov/data-browser/).\n"
        "- **One row** = one mortgage application.\n"
        "- **States:** CA, MA (expensive), FL, TX (mid), MI, OH (low), two per home-price tier.")

    st.header("Step 1: Keep comparable applications", anchor=False)
    st.write("Only first-lien home purchases of a primary, site-built home are kept, so loans can be compared fairly.")
    st.dataframe(pd.read_csv(DATA_DIR / "funnel_scope.csv"))

    st.header("Step 2: Keep approved, comparable loans", anchor=False)
    st.write("Only approved loans have a price. Only 30-year fixed-rate loans are kept, and impossible values are removed.")
    st.dataframe(pd.read_csv(DATA_DIR / "funnel_cleaning.csv"))

    st.header("Key decisions", anchor=False)
    st.markdown(
        "- **Download checked against the source:** the first California and Texas files were incomplete "
        "and were downloaded again.\n"
        "- **No imputation:** denied applications have no price by design, so they are not filled in.\n"
        "- **Exempt lenders removed:** small lenders that don't report some fields were removed, "
           "to keep only confirmed standard loans.\n"
        "- **Medians, not means:** prices are skewed, so medians describe a typical borrower better.")



# ---------------------------------------------------------------
# Tab 6: Limitations
# ---------------------------------------------------------------
with tab_limits:
    st.header("What this data can and can't tell you", anchor=False)
    st.markdown(
        "- **No credit scores.** HMDA does not include credit scores, which strongly affect mortgage rates. "
        "Part of the differences shown may come from credit scores.\n"
        "- **Associations, not causes.** The app shows patterns in past loans; it does not prove that one "
        "factor causes a higher price.\n"
        "- **Past loans, not quotes.** The figures describe 2025 loans, not the rate you would be offered today.\n"
        "- **Six states only.** Results may differ in other states. Both mid-tier states are in the South and "
        "both low-tier states are in the Midwest, so tier differences may partly reflect region.\n"
        "- **Closing costs combine many fees,** so differences may partly reflect the mix of loan types.")
