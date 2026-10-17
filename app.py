from pathlib import Path
import pandas as pd
import streamlit as st

df = pd.read_parquet(Path(__file__).parent / "data" / "processed" / "hmda_2025_pricing_clean.parquet")

st.title("What Makes a Mortgage Cost More?")
st.write("See how the down payment relates to mortgage price (rate spread) in 2025 HMDA data.")

state = st.selectbox("Choose a state", ["CA", "MA", "FL", "TX", "MI", "OH"])

selected = df[df["state_code"] == state]
st.bar_chart(selected.groupby("down_payment_band", observed=True)["rate_spread"].median())
