# Pokémon Database

## Project Overview

The Pokémon Database is a multipage web application built using Python and Streamlit. The application allows users to explore Pokémon statistics, search for Pokémon trading cards, and compare different Pokémon using interactive visualizations.

The purpose of this project is to make Pokémon information easier to search, filter, and understand.

## Features

### Home
- Introduces the Pokémon Database application.
- Displays summary statistics from the dataset.
- Allows users to select a featured Pokémon.
- Uses Session State to save the selected Pokémon.

### Pokémon Index
- Search for Pokémon by name.
- Filter Pokémon by type and minimum Attack value.
- Sort Pokémon based on different statistics.
- View summary metrics based on filtered results.
- Explore Pokémon type distribution through a bar chart.
- View Pokémon information in an interactive table.

### Pokémon TCG
- Search for Pokémon trading cards using the TCGdex API.
- View matching trading cards and their details.
- Display card artwork, rarity, HP, and available pricing information.
- Cache API results to improve performance.
- Handle unsuccessful searches and API errors.

### Pokémon Analytics
- View a bar chart of the ten most common Pokémon type categories.
- Select two Pokémon to compare their battle statistics.
- Compare HP, Attack, Defense, Special Attack, Special Defense, and Speed.
- View an interactive grouped bar chart and comparison table.

## Technologies Used

- **Python** - Main programming language
- **Streamlit** - Web application framework
- **Pandas** - Data loading, filtering, and analysis
- **Plotly** - Interactive data visualizations
- **Requests** - API requests
- **Pillow** - Image handling
- **TCGdex API** - Pokémon trading card information

## Data Sources

The application uses a local Pokémon CSV dataset containing Pokémon names, types, and battle statistics.

It also uses the [TCGdex API](https://tcgdex.dev/) to retrieve Pokémon trading card information, including images, rarity, and available pricing data.

## Project Structure

```text
Pokemon_Assignment/
│
├── Home.py
├── pages/
│   ├── 1_Pokemon_Index.py
│   ├── 2_TCG.py
│   └── 3_Pokemon_Analytics.py
├── data/
│   └── pokemon_data.csv
├── images/
│   └── Pokémon_Charizard_art.png
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/front-end-web-design-.git
```

### 2. Navigate to the Project Folder

```bash
cd front-end-web-design-/Pokemon_Assignment
```

### 3. Install the Required Libraries

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python -m streamlit run Home.py
```

## Session State and Caching

The application uses `st.session_state` to save the selected Pokémon and share that selection between different pages.

It also uses `@st.cache_data` to cache the CSV dataset and API responses, reducing unnecessary loading and improving performance.

## Error Handling

The application includes error handling for unsuccessful API requests and displays messages when searches return no matching results.

## Deployment

The application is deployed using Streamlit Community Cloud and GitHub.

**Main application file:** `Pokemon_Assignment/Home.py`

## Project Purpose

This project demonstrates the use of Python, Streamlit, Pandas, APIs, Session State, caching, and interactive visualizations to build a functional multipage web application.
