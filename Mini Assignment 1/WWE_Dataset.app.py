import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px


# Page configuration
st.set_page_config(
    page_title="WWE Match Explorer",
    page_icon="wwe_logo.png",
    layout="wide"
)


# Page Details
st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #333333;
        color: white;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Main title */
    h1 {
        color: white !important;
        font-weight: 800 !important;
    }

    h2, h3 {
        color: white !important;
        font-weight: 700 !important;
    }

    p {
        color: white !important;
    }

    /* Red section headers */
    .section-header {
        background-color: #8B0000;
        color: white;
        padding: 12px 18px;
        border-radius: 8px;
        margin-top: 10px;
        margin-bottom: 15px;
        font-size: 22px;
        font-weight: bold;
    }

    /* Divider */
    hr {
        border-color: #777777 !important;
    }

    /* Select boxes */
    div[data-baseweb="select"] > div {
        background-color: #eeeeee !important;
        border: 1px solid #555555 !important;
        color: #222222 !important;
    }

    div[data-baseweb="select"] span {
        color: #222222 !important;
    }

    /* Text input */
    div[data-baseweb="input"] > div {
        background-color: #eeeeee !important;
        border: 1px solid #555555 !important;
        color: #222222 !important;
    }

    input {
        color: #222222 !important;
        background-color: #eeeeee !important;
    }

    input::placeholder {
        color: #666666 !important;
    }

    /* RED BUTTONS WITH WHITE TEXT */
    .stButton > button,
    .stFormSubmitButton > button {
        background-color: #8B0000 !important;
        color: white !important;
        border: 1px solid #8B0000 !important;
        border-radius: 6px !important;
        font-weight: bold !important;
    }

    /* Button hover */
    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        background-color: #A00000 !important;
        color: white !important;
        border: 1px solid #A00000 !important;
    }

    /* Metrics */
    div[data-testid="stMetric"] {
        background-color: #8B0000;
        border: 1px solid #555555;
        padding: 15px;
        border-radius: 8px;
    }

    div[data-testid="stMetricLabel"] {
        color: white !important;
    }

    div[data-testid="stMetricValue"] {
        color: white !important;
    }

    /* Expander */
    div[data-testid="stExpander"] {
        background-color: #eeeeee;
        border: 1px solid #555555;
        border-radius: 8px;
    }

    /* Dataframe */
    div[data-testid="stDataFrame"] {
        border: 1px solid #555555;
        border-radius: 6px;
    }

    /* Checkbox */
    div[data-testid="stCheckbox"] label {
        color: white !important;
    }

    /* Form */
    div[data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
        background-color: transparent !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# WWE csv file dataframe
df = pd.read_csv("WWE_History_1000.csv")


# Session state for filters and search input
if "event_filter" not in st.session_state:
    st.session_state.event_filter = "All Events"

if "title_filter" not in st.session_state:
    st.session_state.title_filter = "All Matches"

if "sort_filter" not in st.session_state:
    st.session_state.sort_filter = "Date"

if "ascending" not in st.session_state:
    st.session_state.ascending = True

if "wrestler_input" not in st.session_state:
    st.session_state.wrestler_input = ""

if "submitted_wrestler" not in st.session_state:
    st.session_state.submitted_wrestler = ""

if "reset_filters" not in st.session_state:
    st.session_state.reset_filters = False


# Reset filter values before widgets are created
if st.session_state.reset_filters:

    st.session_state.event_filter = "All Events"
    st.session_state.title_filter = "All Matches"
    st.session_state.sort_filter = "Date"
    st.session_state.ascending = True
    st.session_state.wrestler_input = ""
    st.session_state.submitted_wrestler = ""

    st.session_state.reset_filters = False


# Title
logo_col, title_col = st.columns([1, 6])

with logo_col:
    st.image("wwe_logo.png", width=90)

with title_col:
    st.title("WWE Match Explorer")

st.write(
    "Explore WWE wrestlers match history statistics between 12/31/2022 - 11/4/2023."
)


# Filter section
st.markdown("---")

st.markdown(
    '<div class="section-header"> Filter WWE Matches</div>',
    unsafe_allow_html=True
)


# Event filter
events = [
    "All Events"
] + sorted(
    df["Event"].dropna().unique().tolist()
)

st.selectbox(
    "Select WWE Event",
    events,
    key="event_filter"
)


# Wrestler search and submit button
with st.form("wrestler_search_form"):

    st.text_input(
        "Search Wrestler",
        placeholder="Enter a wrestler name...",
        key="wrestler_input"
    )

    search_clicked = st.form_submit_button(
        "Search Wrestler"
    )

    if search_clicked:

        st.session_state.submitted_wrestler = (
            st.session_state.wrestler_input.strip()
        )


# Title match or non-title match filter
st.selectbox(
    "Match Type",
    [
        "All Matches",
        "Title Matches Only",
        "Non-Title Matches Only"
    ],
    key="title_filter"
)


# Sort filter
st.selectbox(
    "Sort By",
    [
        "Date",
        "Event",
        "Winner",
        "Loser"
    ],
    key="sort_filter"
)


# Ascending order checkbox
st.checkbox(
    "Ascending Order",
    key="ascending"
)


# Reset filters button
if st.button("Reset Filters"):

    st.session_state.reset_filters = True

    st.rerun()


# Apply filters to the dataframe
filtered = df.copy()


# Event filter state
if st.session_state.event_filter != "All Events":

    filtered = filtered[
        filtered["Event"] == st.session_state.event_filter
    ]


# Title match filter state
if st.session_state.title_filter == "Title Matches Only":

    filtered = filtered[
        filtered["Title Match"]
        .astype(str)
        .str.lower()
        == "yes"
    ]

elif st.session_state.title_filter == "Non-Title Matches Only":

    filtered = filtered[
        filtered["Title Match"]
        .astype(str)
        .str.lower()
        == "no"
    ]


# Wrestler search filter state
submitted_wrestler = (
    st.session_state.submitted_wrestler
)


if submitted_wrestler:

    winner_matches = (
        filtered["Winner"]
        .astype(str)
        .str.contains(
            submitted_wrestler,
            case=False,
            na=False
        )
    )

    loser_matches = (
        filtered["Loser"]
        .astype(str)
        .str.contains(
            submitted_wrestler,
            case=False,
            na=False
        )
    )

    # Show matches where wrestler is either the winner or loser
    filtered = filtered[
        winner_matches | loser_matches
    ]


# Sort the filtered dataframe
filtered = filtered.sort_values(
    by=st.session_state.sort_filter,
    ascending=st.session_state.ascending
)


# Match statistics
st.markdown("---")

st.markdown(
    '<div class="section-header"> Match Statistics</div>',
    unsafe_allow_html=True
)


matches_shown = len(filtered)


# Count opponents when a wrestler is searched
if submitted_wrestler:

    wrestler = submitted_wrestler.lower()

    opponents = []

    for _, row in filtered.iterrows():

        winner = str(row["Winner"])
        loser = str(row["Loser"])

        if winner.lower() == wrestler:

            opponents.append(loser)

        elif loser.lower() == wrestler:

            opponents.append(winner)

    opponents_shown = len(set(opponents))

else:

    opponents_shown = 0


# Count title matches
title_matches = (
    filtered["Title Match"]
    .astype(str)
    .str.lower()
    .eq("yes")
    .sum()
)


metric1, metric2, metric3 = st.columns(3)


with metric1:

    st.metric(
        "Matches Shown",
        matches_shown
    )


with metric2:

    st.metric(
        "Opponents Shown",
        opponents_shown
    )


with metric3:

    st.metric(
        "Title Matches",
        title_matches
    )


# WWE Match Analytics
st.markdown("---")

st.markdown(
    '<div class="section-header"> WWE Match Analytics</div>',
    unsafe_allow_html=True
)


# Altair chart for Title Matches vs Non-Title Matches by Event
st.subheader(
    "Title Matches vs Non-Title Matches by Event"
)


if not filtered.empty:

    event_chart_data = filtered.copy()

    event_chart_data["Match_Type"] = (
        event_chart_data["Title Match"]
        .map(
            {
                "Yes": "Title Match",
                "No": "Non-Title Match"
            }
        )
    )


    # Aggregate data
    event_data = (
        event_chart_data
        .groupby(
            ["Event", "Match_Type"]
        )
        .size()
        .reset_index(
            name="Matches"
        )
    )


    # Horizontal Altair bar chart
    altair_chart = (
        alt.Chart(event_data)
        .mark_bar()
        .encode(

            x=alt.X(
                "Matches:Q",
                title="Number of Matches"
            ),

            y=alt.Y(
                "Event:N",
                sort="-x",
                title="WWE Event"
            ),

            color=alt.Color(
                "Match_Type:N",
                title="Match Type"
            ),

            tooltip=[
                "Event",
                "Match_Type",
                "Matches"
            ]
        )
        .properties(
            height=450,
            title="Title Matches vs Non-Title Matches"
        )
    )


    st.altair_chart(
        altair_chart,
        use_container_width=True
    )

else:

    st.info(
        "There is no data available for the selected filters."
    )


# Plotly chart for Wins vs Losses
st.subheader(
    "Wrestler Wins vs Losses"
)


if not submitted_wrestler:

    st.info(
        "Search for a wrestler above to see their wins and losses."
    )

else:

    # Find wrestler names matching the search
    winner_names = (
        filtered["Winner"]
        .dropna()
        .astype(str)
    )

    loser_names = (
        filtered["Loser"]
        .dropna()
        .astype(str)
    )


    matching_winners = winner_names[
        winner_names.str.contains(
            submitted_wrestler,
            case=False,
            na=False
        )
    ].unique().tolist()


    matching_losers = loser_names[
        loser_names.str.contains(
            submitted_wrestler,
            case=False,
            na=False
        )
    ].unique().tolist()


    matching_names = sorted(
        set(
            matching_winners
            + matching_losers
        )
    )


    # Show wins vs losses for the wrestler
    if len(matching_names) == 1:

        wrestler = matching_names[0]


        # Count wins
        wins = (
            filtered["Winner"]
            .astype(str)
            .str.lower()
            .eq(
                wrestler.lower()
            )
            .sum()
        )


        # Count losses
        losses = (
            filtered["Loser"]
            .astype(str)
            .str.lower()
            .eq(
                wrestler.lower()
            )
            .sum()
        )


        # Chart data
        wrestler_data = pd.DataFrame(
            {
                "Result": [
                    "Wins",
                    "Losses"
                ],

                "Matches": [
                    wins,
                    losses
                ]
            }
        )


        # Create the pie chart
        pie_chart = px.pie(
            wrestler_data,
            names="Result",
            values="Matches",
            title=f"{wrestler}: Wins vs Losses",
            hole=0.35
        )


        pie_chart.update_traces(
            textinfo="percent+label"
        )


        pie_chart.update_layout(
            legend_title_text="Result"
        )


        st.plotly_chart(
            pie_chart,
            use_container_width=True
        )


    # No wrestler found
    else:

        st.info(
            "No wrestler was found, check your spelling."
        )


# Filtered WWE Matches Table
st.markdown("---")

st.markdown(
    '<div class="section-header">WWE Filtered Matches</div>',
    unsafe_allow_html=True
)


if filtered.empty:

    st.warning(
        "No matches match the selected filters."
    )

else:

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )


# Footer caption
st.caption(
    "WWE Match Explorer | Mini Assignment 1"
)
