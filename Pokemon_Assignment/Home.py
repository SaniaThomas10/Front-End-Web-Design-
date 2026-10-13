
import streamlit as st 
import pandas as pd
from PIL import Image


#page configuration
charzard_image = Image.open("images/Pokémon_Charizard_art.png") #Logo picture 

st.set_page_config(page_title="Pokemon Database", page_icon=charzard_image, layout="wide")



#load data 
@st.cache_data
def load_data():
    df = pd.read_csv("data/pokemon_data.csv")
    return df 

df = load_data() #call to load the data



#Session state 
if "selected_pokemon" not in st.session_state:
    st.session_state.selected_pokemon = None



#Page header 
logo_col, title_col = st.columns([1, 10])

with logo_col:
    st.image(charzard_image, width=100)

with title_col:
    st.title("Pokemon Database")

st.write("Discover Pokemon, explore their battle statistics, and take a look at their prices/values")

st.divider()



#problem statement 
st.header("The Problem")

st.write("Pokemon fans and collectors often struggle to find a comprehensive database that provides detailed information about each Pokemon, including their battle statistics, types, and market values. This lack of accessible information can hinder their ability to make informed decisions when it comes to collecting or battling with Pokemon while playing the game.")

st.divider()



#Overview of the Dataset
st.header("Overview of the Dataset")

st.write("The dataset used in this project is a collection of information about various Pokemon species. It includes their names, types, and battle statistics such as HP, Attack, Defense, Special Attack, Special Defense, and Speed. Pokemon trading card information and available market prices will be retrieved separately from the TCG API.")



total_entries = len(df) #number of rows 

unique_pokemon = df['Name'].nunique() #number of unique pokemon names

average_hp = df['HP'].mean() #the average HP of all the pokemon in the dataset

average_attack = df['Attack'].mean() #the average attack of all the pokemon in the dataset



#Display metrics 
metric_columns = st.columns(4) #create 4 columns for the metrics

with metric_columns[0]:
    st.metric("Total Entries", total_entries)

with metric_columns[1]:
    st.metric("Unique Pokemon", unique_pokemon)

with metric_columns[2]:
    st.metric("Average HP", f"{average_hp:.2f}")

with metric_columns[3]:
    st.metric("Average Attack", f"{average_attack:.2f}")

st.divider()



#Featured Pokemon Section
st.header("Featured Pokemon")

st.write("Pick the pokemon you want to learn more about from the dropdown below. You can explore their battle statistics and types. Trading card information and available prices will be shown on the TCG page.")

known_pokemon = df["Name"].dropna() # get the names of the pokemon without any null values

unique_names = known_pokemon.unique() #get the unique names of the pokemon

pokemon_names = sorted(unique_names) #sort the names in alphabetical order


if len(pokemon_names) == 0: #check if there are any pokemon names in the dataset
    st.warning("No Pokemon names found in the dataset.")

    st.stop() 



#dropdown for selecting a pokemon
pokemon_options = ["Choose A Pokemon:"] + pokemon_names #default prompt 

current_selection = st.session_state.selected_pokemon #get the current selection from the session state

if current_selection in pokemon_options:
    default_index = pokemon_options.index(current_selection) #get the index of the current selection

else:
    default_index = 0 #default to the first option if the current selection is not in the options


#dropdown
selected_pokemon = st.selectbox("Choose A Pokemon:", options=pokemon_options, index=default_index)


#save the pokemon in the session state 
if selected_pokemon == "Choose A Pokemon:":
    st.session_state.selected_pokemon = None

else:
    st.session_state.selected_pokemon = selected_pokemon



#Filter the dataset 
if st.session_state.selected_pokemon is None: # Filter the dataset when a pokemon is picked, or show the message to pick one 

    st.info("Pick a Pokemon to Show its Details")

else: #filtering the dataset to show the selected pokemon's details 

    filtered = df.copy() #create a copy of the dataset to filter

    filtered = filtered[filtered["Name"] == st.session_state.selected_pokemon] #filter the dataset to show the selected pokemon's details


    if filtered.empty: #check if the filtered dataset is empty
        st.warning("No data found for the selected Pokemon.")

    else: 
        pokemon = filtered.iloc[0] #get the first row of the filtered dataset

        info_col, stats_col = st.columns(2) #create two columns for the pokemon's information and stats


        #Pokemon Information
        with info_col:
            st.subheader("Pokemon Information")
            st.write(f"**Name:** {pokemon['Name']}")
            st.write(f"**Pokedex Number:** {pokemon['No']}")
            st.write(f"**Type:** {pokemon['Type']}")
            st.write(f"**Total Stats:** {pokemon['Total']}")


        #Battle Statistics
        with stats_col:
            st.subheader("Battle Statistics")
            st.write(f"**HP:** {pokemon['HP']}")
            st.write(f"**Attack:** {pokemon['Attack']}")
            st.write(f"**Defense:** {pokemon['Defense']}")
            st.write(f"**Special Atk:** {pokemon['Sp. Atk']}")
            st.write(f"**Special Def:** {pokemon['Sp. Def']}")
            st.write(f"**Speed:** {pokemon['Speed']}")
