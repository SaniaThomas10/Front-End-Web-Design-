import pandas as pd
import streamlit as st



# Load Spotify data

@st.cache_data
def load_data():

    # Read the Spotify CSV file.
    df = pd.read_csv(
        "data/most_streamed_spotify_2025.csv"
    )

    return df


# Format large numbers
def format_number(number):

    if number >= 1_000_000_000:

        return f"{number / 1_000_000_000:.2f}B"


    elif number >= 1_000_000:

        return f"{number / 1_000_000:.2f}M"


    elif number >= 1_000:

        return f"{number / 1_000:.1f}K"


    else:

        return f"{number:,.0f}"


# website style

def apply_style():

    st.markdown(
        """
        <style>

        /* Make buttons Spotify green */
        [data-testid="stButton"] button {
            background-color: #1DB954 !important;
            color: white !important;
            border: none !important;
            font-weight: bold !important;
            border-radius: 8px !important;
        }


        /* Brighter green when hovering */
        [data-testid="stButton"] button:hover {
            background-color: #1ED760 !important;
            color: white !important;
            border: none !important;
        }


        /* Keep headings white */
        h1, h2, h3 {
            color: white;
        }


        /* Keep regular text white */
        p {
            color: white;
        }


        </style>
        """,
        unsafe_allow_html=True
    )