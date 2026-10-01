import streamlit as st

from utils.data import load_data, format_number, apply_style


# Page configuration
st.set_page_config(
    page_title="Spotify 2025 Explorer",
    page_icon="images/spotify_logo.png",
    layout="wide"
)


# Website style
apply_style()



# Load data
df = load_data()


# Session state
if "selected_artist" not in st.session_state:
    st.session_state.selected_artist = "All Artists"



# Header
logo_column, title_column = st.columns(
    [1, 10],
    vertical_alignment="center"
)


with logo_column:

    st.image(
        "images/spotify_logo.png",
        width=70
    )


with title_column:

    st.title(
        "Spotify 2025 Explorer"
    )


st.write(
    "Explore the songs, artists, and streaming patterns "
    "in Spotify's 2025 streaming data."
)


st.divider()



# Problem statement

st.header("The Problem")


st.write(
    """
    Music listeners can easily see which songs are popular,
    but it can be harder to understand how artists and songs
    compare across a large streaming dataset.

    Spotify 2025 Explorer helps music listeners explore the
    most-streamed songs of 2025 by making the data easier to
    filter, compare, and understand.
    """
)


# Dataset overview

total_songs = len(df)

total_artists = df["artist"].nunique()

total_streams = df["spotify_streams_total"].sum()

average_streams = df["spotify_streams_total"].mean()


# Green dataset heading

st.markdown(
    """
    <h2 style="
        color: #1DB954;
        margin-bottom: 25px;
    ">
        Dataset at a Glance
    </h2>
    """,
    unsafe_allow_html=True
)



# Green dataset metrics

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(
        f"""
        <p style="
            color: #1DB954;
            font-size: 16px;
            margin-bottom: 5px;
        ">
            Songs
        </p>

        <p style="
            color: #1DB954;
            font-size: 32px;
            margin-top: 0px;
        ">
            {total_songs}
        </p>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <p style="
            color: #1DB954;
            font-size: 16px;
            margin-bottom: 5px;
        ">
            Artists
        </p>

        <p style="
            color: #1DB954;
            font-size: 32px;
            margin-top: 0px;
        ">
            {total_artists}
        </p>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f"""
        <p style="
            color: #1DB954;
            font-size: 16px;
            margin-bottom: 5px;
        ">
            Total Streams
        </p>

        <p style="
            color: #1DB954;
            font-size: 32px;
            margin-top: 0px;
        ">
            {format_number(total_streams)}
        </p>
        """,
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        f"""
        <p style="
            color: #1DB954;
            font-size: 16px;
            margin-bottom: 5px;
        ">
            Average Streams per Song
        </p>

        <p style="
            color: #1DB954;
            font-size: 32px;
            margin-top: 0px;
        ">
            {format_number(average_streams)}
        </p>
        """,
        unsafe_allow_html=True
    )


st.divider()


# Most-streamed songs

st.header("Most-Streamed Songs")


# Sort songs by total streams and keep the top 10.
top_songs = df.sort_values(
    "spotify_streams_total",
    ascending=False
).head(10)


# Make a copy for displaying the table.
display_top_songs = top_songs.copy()


# Change True and False collaboration values
# into Yes and No.
display_top_songs["is_collaboration"] = (
    display_top_songs[
        "is_collaboration"
    ].map(
        {
            True: "Yes",
            False: "No"
        }
    )
)


# Give the columns user-friendly names.
display_top_songs = display_top_songs.rename(
    columns={
        "rank": "Rank",
        "track": "Song",
        "artist": "Artist",
        "is_collaboration": "Collaboration",
        "spotify_streams_total": "Total Streams",
        "daily_streams": "Daily Streams"
    }
)


# Select columns for the table

table_data = display_top_songs[
    [
        "Rank",
        "Song",
        "Artist",
        "Collaboration",
        "Total Streams",
        "Daily Streams"
    ]
]



# Style the table

styled_table = table_data.style.set_table_styles(
    [
        {
            "selector": "thead th",
            "props": [
                ("background-color", "#1DB954"),
                ("color", "black"),
                ("font-weight", "bold"),
                ("border", "1px solid #999999")
            ]
        },
        {
            "selector": "tbody td",
            "props": [
                ("background-color", "#E5E5E5"),
                ("color", "black"),
                ("border", "1px solid #BDBDBD")
            ]
        }
    ]
)


# Display the table

st.dataframe(
    styled_table,
    hide_index=True,
    width="stretch"
)


st.caption(
    "This table shows the ten songs with the highest "
    "total Spotify stream counts in the dataset."
)



# Dataset information
with st.expander(
    "Where's this data is From?"
):

    st.write(
        """
        This project uses the Most Streamed Spotify Songs 2025
        dataset from Kaggle.

        The dataset contains 730 songs and includes each song's
        artist, Spotify rank, total streams, daily streams,
        collaboration status, and other streaming information.

        https://www.kaggle.com/datasets/kylefengkfeng209/most-streamed-spotify-songs-2025/data
        """
    )




