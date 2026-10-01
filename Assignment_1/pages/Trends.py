from pathlib import Path

import streamlit as st
import plotly.express as px

from utils.data import load_data, format_number, apply_style


project_folder = Path(__file__).resolve().parent.parent

spotify_logo = (
    project_folder
    / "images"
    / "spotify_logo.png"
)


# Page configuration
st.set_page_config(
    page_title="Spotify Trends",
    page_icon=spotify_logo,
    layout="wide"
)


# Website styling
apply_style()



# Load data
df = load_data()



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

    st.title("Spotify Trends")


st.write(
    "Compare artists, songs, and collaborations "
    "using Spotify streaming data."
)


st.divider()


# Tabs
artist_tab, daily_tab, collaboration_tab = st.tabs(
    [
        ":green[Artist Performance]",
        ":green[Daily Streaming]",
        ":green[Collaborations]"
    ]
)


# Artist Performance 
with artist_tab:

    st.header(
        "Which Artists Have the Most Streams?"
    )


    # Group songs by artist
    artist_summary = (
        df.groupby("artist")[
            "spotify_streams_total"
        ]
        .sum()
        .reset_index()
    )


    # Sort artists from highest to lowest streams.
    artist_summary = artist_summary.sort_values(
        "spotify_streams_total",
        ascending=False
    )


    # Keep the top 10 artists.
    top_artists = artist_summary.head(10)

    
    # Artist chart
  

    chart = px.bar(
        top_artists,
        x="artist",
        y="spotify_streams_total",
        labels={
            "artist": "Artist",
            "spotify_streams_total": "Total Streams"
        },
        color_discrete_sequence=[
            "#1DB954"
        ]
    )


    # Rotate artist names so they are easier to read.
    chart.update_layout(
        xaxis_tickangle=-45
    )


    st.plotly_chart(
        chart,
        width="stretch"
    )


    st.caption(
        "This chart groups all songs by artist and adds "
        "their Spotify streams together. It shows the ten "
        "artists with the highest combined stream counts."
    )


    # Artist table
    artist_display = top_artists.rename(
        columns={
            "artist": "Artist",
            "spotify_streams_total": "Total Streams"
        }
    )


    st.subheader(
        "Artist Data"
    )


    st.dataframe(
        artist_display,
        hide_index=True
    )


# Daily Streaming
with daily_tab:

    st.header(
        "Which Songs Are Getting the Most Daily Streams?"
    )


    # Find top songs by daily streams
    daily_songs = df.sort_values(
        "daily_streams",
        ascending=False
    ).head(10)


    # Daily streaming chart
    chart = px.bar(
        daily_songs,
        x="track",
        y="daily_streams",
        labels={
            "track": "Song",
            "daily_streams": "Daily Streams"
        },
        hover_data=[
            "artist"
        ],
        color_discrete_sequence=[
            "#1ED760"
        ]
    )


    # Rotate song names so they are easier to read.
    chart.update_layout(
        xaxis_tickangle=-45
    )


    st.plotly_chart(
        chart,
        width="stretch"
    )


    st.caption(
        "This chart shows the ten songs receiving "
        "the most daily streams in the dataset."
    )


    # Daily stream summary metric
    top_daily_average = daily_songs[
        "daily_streams"
    ].mean()


    st.metric(
        "Average Daily Streams Among These Songs",
        format_number(
            top_daily_average
        )
    )


#Collaborations
with collaboration_tab:

    st.header(
        "How Many Songs Are Collaborations?"
    )


    # Count collaborations
    collaboration_summary = (
        df["is_collaboration"]
        .value_counts()
        .reset_index()
    )


    collaboration_summary.columns = [
        "is_collaboration",
        "Song Count"
    ]


    # Change True and False into Yes and No.
    collaboration_summary[
        "Collaboration"
    ] = collaboration_summary[
        "is_collaboration"
    ].map(
        {
            True: "Yes",
            False: "No"
        }
    )


    # Collaboration pie chart
    chart = px.pie(
        collaboration_summary,
        names="Collaboration",
        values="Song Count",
        title="Collaboration Breakdown",
        color="Collaboration",
        color_discrete_map={
            "No": "#1DB954",
            "Yes": "#1ED760"
        }
    )


    # Show percentage and label inside the pie chart.
    chart.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )


    st.plotly_chart(
        chart,
        width="stretch"
    )


    st.caption(
        "This pie chart shows the percentage of songs "
        "that are collaborations compared with songs "
        "that are not."
    )


    # Collaboration table
    collaboration_display = collaboration_summary[
        [
            "Collaboration",
            "Song Count"
        ]
    ]


    st.subheader(
        "Collaboration Data"
    )


    st.dataframe(
        collaboration_display,
        hide_index=True
    )
