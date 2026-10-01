# Spotify 2025 Explorer

Spotify 2025 Explorer is a multi-page Streamlit application that allows users to explore Spotify streaming data from 2025.

The application makes a large music streaming dataset easier to understand by allowing users to search for songs, filter artists, compare streaming activity, view trends, and discover additional music.

---

## The Problem

Music listeners can easily see which songs are popular, but it can be harder to understand how artists and songs compare across a large streaming dataset.

Spotify 2025 Explorer helps music listeners explore the most-streamed songs of 2025 by making the data easier to filter, compare, and understand.

---

## Features

### Home

The Home page introduces the application and provides an overview of the Spotify dataset.

Users can view:

- Total number of songs
- Total number of artists
- Total Spotify streams
- Average streams per song
- Top 10 most-streamed songs

### Explore Songs

The Explore Songs page allows users to interact with the Spotify dataset using multiple filters.

Users can:

- Select an artist
- Filter between solo songs and collaborations
- Choose a total stream range
- Search for a song by name
- Sort songs by total streams, daily streams, or Spotify rank

The filters work together to help users narrow down the dataset.

### Spotify Trends

The Spotify Trends page uses data visualizations to make streaming patterns easier to understand.

The page includes:

- Top artists by total streams
- Top songs by daily streams
- Collaboration breakdown
- Aggregated artist data
- Streaming summary metrics

### Music Explorer

The Music Explorer page allows users to discover additional music from artists found in the Spotify dataset.

The user selects an artist and the application uses the iTunes Search API to find additional songs from that artist.

Search results include:

- Song name
- Artist
- Album
- Genre

---

## Dataset

This project uses the **Most Streamed Spotify Songs 2025** dataset from Kaggle.

Dataset:
https://www.kaggle.com/datasets/kylefengkfeng209/most-streamed-spotify-songs-2025

The dataset contains 730 songs and includes information such as:

- Spotify rank
- Song name
- Artist
- Total streams
- Daily streams
- Collaboration status
- Daily stream share

---

## API

The application uses the **iTunes Search API**.

The API allows the Music Explorer page to search for additional songs related to an artist selected from the Spotify dataset.

The API request is made using Python's `requests` library and the results are converted into a Pandas DataFrame for display in Streamlit.

API searches are cached using `st.cache_data`.

---

## Technologies Used

- Python
- Streamlit
- Pandas
- Plotly
- Requests
- iTunes Search API
- GitHub
- Streamlit Community Cloud

---

## Project Structure

```text
Assignment_1/
│
├── Home.py
├── requirements.txt
│
├── data/
│   └── most_streamed_spotify_2025.csv
│
├── images/
│   └── spotify_logo.png
│
├── pages/
│   ├── 1_Explore.py
│   ├── 2_Trends.py
│   └── 3_Music_Explorer.py
│
└── utils/
    ├── __init__.py
    └── data.py
