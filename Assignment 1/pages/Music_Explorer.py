import streamlit as st
import pandas as pd
import requests

from utils.data import load_data, apply_style



# Page configuration
st.set_page_config(
    page_title="Music Explorer",
    page_icon="images/spotify_logo.png",
    layout="wide"
)


# Website styling
apply_style()


# Load Spotify data
df = load_data()



# Session state
if "selected_artist" not in st.session_state:
    st.session_state.selected_artist = "All Artists"


if "search_results" not in st.session_state:
    st.session_state.search_results = None


# iTunes Search API

@st.cache_data
def search_itunes(artist):

    # Public iTunes Search API.
    url = "https://itunes.apple.com/search"


    # Information sent with the API request.
    params = {
        "term": artist,
        "entity": "song",
        "limit": 20
    }


    # Send GET request to the API.
    response = requests.get(
        url,
        params=params,
        timeout=10
    )


    # Check that the request worked.
    response.raise_for_status()


    # Convert the JSON response into Python data.
    data = response.json()


    # Get the song results.
    results = data["results"]


    # Convert the results into a DataFrame.
    return pd.DataFrame(results)



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

    st.title("Music Explorer")


st.write(
    "Choose an artist from the Spotify dataset to discover "
    "more of their music using the iTunes Search API."
)


st.divider()



# Choose an artist

st.markdown(
    """
    <h2 style="
        color: #1DB954;
        margin-bottom: 20px;
    ">
        Choose an Artist
    </h2>
    """,
    unsafe_allow_html=True
)


# Get all artists from the Spotify dataset.
artist_values = df["artist"].dropna()


# Get each artist only once.
unique_artists = artist_values.unique()


# Put the artists in alphabetical order.
sorted_artists = sorted(unique_artists)


# Add an All Artists option.
artist_options = [
    "All Artists"
] + sorted_artists



# Restore artist from session state
current_artist = st.session_state.selected_artist


# Make sure the saved artist still exists.
if current_artist not in artist_options:

    current_artist = "All Artists"


# Find the artist's position in the dropdown.
artist_index = artist_options.index(
    current_artist
)


# Green dropdown label
st.markdown(
    """
    <p style="
        color: #1DB954;
        font-size: 16px;
        margin-bottom: 5px;
    ">
        Which Spotify artist would you like to search for?
    </p>
    """,
    unsafe_allow_html=True
)


# Artist dropdown
selected_artist = st.selectbox(
    "Which Spotify artist would you like to search for?",
    artist_options,
    index=artist_index,
    label_visibility="collapsed"
)


# Save the artist choice.
st.session_state.selected_artist = (
    selected_artist
)


# Search button

if st.button("Search"):

    # Make sure an artist was selected.
    if selected_artist == "All Artists":

        st.warning(
            "Choose an artist before searching."
        )


    else:

        try:

            # Search the iTunes API.
            st.session_state.search_results = (
                search_itunes(
                    selected_artist
                )
            )


        except requests.RequestException:

            st.error(
                "The music service could not be reached. "
                "Please try again."
            )


# Search results
results = st.session_state.search_results


if results is not None:

    # Empty results
    if len(results) == 0:

        st.info(
            "No songs were found for this artist. "
            "Try another artist."
        )

        st.stop()



    # Display results
    st.header("Search Results")


    st.write(
        f"{len(results)} songs found."
    )


    # Keep only the columns we want to show.
    music_results = results[
        [
            "trackName",
            "artistName",
            "collectionName",
            "primaryGenreName"
        ]
    ].copy()


    # Rename columns so they are easier to understand.
    music_results = music_results.rename(
        columns={
            "trackName": "Song",
            "artistName": "Artist",
            "collectionName": "Album",
            "primaryGenreName": "Genre"
        }
    )


    # Display the results.
    st.dataframe(
        music_results,
        hide_index=True
    )


    st.caption(
        "These results come from the public "
        "iTunes Search API."
    )


# API Summury  
with st.expander(
    "iTunes Search API"
):

    st.markdown(
        """
        :green[The iTunes Search API helps you discover more music
        from an artist you find in the Spotify 2025 dataset.]

        :green[After selecting an artist and clicking Search, the
        Music Explorer searches iTunes for songs related to
        that artist.]

        :green[The results show up to 20 songs and include the song
        name, artist, album, and genre. This allows you to go
        beyond the songs in the Spotify dataset and explore
        more music from artists that interest you.]
        """
    )
