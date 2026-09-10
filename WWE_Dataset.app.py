import streamlit as st
import pandas as pd

st.title("WWE Match History Explorer")
st.write("Explore WWE match history using filters.")

# Load the dataset
df = pd.read_csv("WWE_History_1000.csv")

# Display the full dataset
st.subheader("WWE Match Data")
st.dataframe(df, width="stretch")

# Filter 1: Event dropdown
st.subheader("Filters")

events = ["All Events"] + sorted(df["Event"].dropna().unique().tolist())

selected_event = st.selectbox(
    "Choose a WWE Event:",
    events
)

filtered = df.copy()

if selected_event != "All Events":
    filtered = filtered[
        filtered["Event"] == selected_event
    ]

# Filter 2: Winner search
winner_search = st.text_input(
    "Search by Winner:"
)

if winner_search:
    filtered = filtered[
        filtered["Winner"].astype(str).str.contains(
            winner_search,
            case=False,
            na=False
        )
    ]

# Display filtered data
st.subheader("Filtered Results")
st.write(f"Showing {len(filtered)} matches")

st.dataframe(
    filtered,
    width="stretch"
)