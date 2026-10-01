from pathlib import Path

import streamlit as st

from utils.data import load_data, format_number, apply_style


project_folder = Path(__file__).resolve().parent.parent

spotify_logo = (
    project_folder
    / "images"
    / "spotify_logo.png"
)


# Page configuration
st.set_page_config(
    page_title="Explore Songs",
    page_icon=spotify_logo,
    layout="wide"
)



# Website styling
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
        spotify_logo,
        width=70
    )


with title_column:

    st.title("Explore Songs")


st.write(
    "Choose different filters to find songs and artists "
    "that interest you."
)


st.divider()



# Filters

st.header("Filter Songs")


# Put the first two filters next to each other.
filter_col1, filter_col2 = st.columns(2)


# Artist filter
with filter_col1:

    artist_values = df["artist"].dropna()

    unique_artists = artist_values.unique()

    sorted_artists = sorted(unique_artists)

    artist_options = [
        "All Artists"
    ] + sorted_artists


    current_artist = (
        st.session_state.selected_artist
    )


    if current_artist not in artist_options:

        current_artist = "All Artists"


    artist_index = artist_options.index(
        current_artist
    )


    selected_artist = st.selectbox(
        "Which artist would you like to explore?",
        artist_options,
        index=artist_index
    )


    # Save artist choice in session state.
    st.session_state.selected_artist = (
        selected_artist
    )


# Collaboration filter
with filter_col2:

    song_type = st.selectbox(
        "What type of songs would you like to see?",
        [
            "All Songs",
            "Solo Songs",
            "Collaborations"
        ]
    )



# Stream range
minimum_streams = int(
    df["spotify_streams_total"].min()
)


maximum_streams = int(
    df["spotify_streams_total"].max()
)


stream_range = st.slider(
    "What range of total streams would you like to see?",
    min_value=minimum_streams,
    max_value=maximum_streams,
    value=(
        minimum_streams,
        maximum_streams
    )
)


# Search and sort
search_col, sort_col = st.columns(2)


with search_col:

    song_search = st.text_input(
        "Search for a song by name",
        placeholder="Enter a song name"
    )


with sort_col:

    sort_choice = st.selectbox(
        "How would you like to sort the songs?",
        [
            "Most total streams",
            "Most daily streams",
            "Spotify rank"
        ]
    )


st.divider()


# Apply filters
filtered_df = df.copy()


# Artist filter
if selected_artist != "All Artists":

    filtered_df = filtered_df[
        filtered_df["artist"]
        == selected_artist
    ]


# Collaboration filter
if song_type == "Solo Songs":

    filtered_df = filtered_df[
        filtered_df["is_collaboration"]
        == False
    ]


elif song_type == "Collaborations":

    filtered_df = filtered_df[
        filtered_df["is_collaboration"]
        == True
    ]


# Stream range filter
filtered_df = filtered_df[
    filtered_df[
        "spotify_streams_total"
    ].between(
        stream_range[0],
        stream_range[1]
    )
]


# Song name filter
if song_search != "":

    filtered_df = filtered_df[
        filtered_df["track"].str.contains(
            song_search,
            case=False,
            na=False
        )
    ]


# Sort filtered data
if sort_choice == "Most total streams":

    filtered_df = filtered_df.sort_values(
        "spotify_streams_total",
        ascending=False
    )


elif sort_choice == "Most daily streams":

    filtered_df = filtered_df.sort_values(
        "daily_streams",
        ascending=False
    )


else:

    filtered_df = filtered_df.sort_values(
        "rank",
        ascending=True
    )


# Empty result handling
if len(filtered_df) == 0:

    st.warning(
        "No songs match those filters. "
        "Try changing one of your choices."
    )

    st.stop()


# Summary metrics
number_of_songs = len(
    filtered_df
)


average_streams = filtered_df[
    "spotify_streams_total"
].mean()


average_daily_streams = filtered_df[
    "daily_streams"
].mean()


# Green results heading
st.markdown(
    """
    <h2 style="
        color: #1DB954;
        margin-bottom: 25px;
    ">
        Your Results
    </h2>
    """,
    unsafe_allow_html=True
)


# Green result metrics

col1, col2, col3 = st.columns(3)


with col1:

    st.markdown(
        f"""
        <p style="
            color: #1DB954;
            font-size: 16px;
            margin-bottom: 5px;
        ">
            Songs Found
        </p>

        <p style="
            color: #1DB954;
            font-size: 32px;
            font-weight: 400;
            margin-top: 0px;
        ">
            {number_of_songs}
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
            Average Total Streams
        </p>

        <p style="
            color: #1DB954;
            font-size: 32px;
            font-weight: 400;
            margin-top: 0px;
        ">
            {format_number(average_streams)}
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
            Average Daily Streams
        </p>

        <p style="
            color: #1DB954;
            font-size: 32px;
            font-weight: 400;
            margin-top: 0px;
        ">
            {format_number(average_daily_streams)}
        </p>
        """,
        unsafe_allow_html=True
    )



# Prepare table for display

display_df = filtered_df.copy()


# Change True and False into Yes and No.
display_df["is_collaboration"] = (
    display_df[
        "is_collaboration"
    ].map(
        {
            True: "Yes",
            False: "No"
        }
    )
)


# Give columns user-friendly names.
display_df = display_df.rename(
    columns={
        "rank": "Rank",
        "track": "Song",
        "artist": "Artist",
        "is_collaboration":
            "Collaboration",
        "spotify_streams_total":
            "Total Streams",
        "daily_streams":
            "Daily Streams"
    }
)


# Results table

st.subheader("Songs")


st.dataframe(
    display_df[
        [
            "Rank",
            "Song",
            "Artist",
            "Collaboration",
            "Total Streams",
            "Daily Streams"
        ]
    ],
    hide_index=True
)


st.caption(
    "The table updates automatically "
    "when you change the filters."
)


# Table key
with st.expander(
    "Table Key"
):

    st.markdown(
        """
        :green[**Rank:** The song's overall rank in the Spotify dataset.]

        :green[**Song:** The name of the song.]

        :green[**Artist:** The artist credited for the song.]

        :green[**Collaboration:** Yes means the song is a collaboration.
        No means it is not a collaboration.]

        :green[**Total Streams:** The total number of Spotify streams
        recorded for the song.]

        :green[**Daily Streams:** The number of daily streams recorded
        for the song.]
        """
    )
