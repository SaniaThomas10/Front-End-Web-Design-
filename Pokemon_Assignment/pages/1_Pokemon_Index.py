
import streamlit as st
import pandas as pd
from PIL import Image


#page configuration
charzard_image = Image.open("Pokemon_Assignment/images/Pokémon_Charizard_art.png") #Logo picture

st.set_page_config(page_title="Pokemon Index", page_icon=charzard_image, layout="wide")


#load data
@st.cache_data
def load_data():
    df = pd.read_csv("Pokemon_Assignment/data/pokemon_data.csv")
    return df

df = load_data()


#session state
if "selected_pokemon" not in st.session_state: # so Streamlit remembers the selected pokemon when navigating between pages
    st.session_state.selected_pokemon = None


#Page header
logo_col, title_col = st.columns([1, 10])

with logo_col:
    st.image(charzard_image, width=100)

with title_col:
    st.title("Pokemon Index")

st.write("Find your favorite Pokemon, explore their types and battle statistics, and compare them.")

st.divider()


#search and filters
st.header("Find a Pokemon")

st.write("Use the filters to narrow down your search.")


#name search
#get the pokemon names from the dataset
pokemon_names = sorted(df['Name'].dropna().unique())

pokemon_options = ["All Pokemon"] + pokemon_names


#get the saved pokemon from the other pages
saved_pokemon = st.session_state.selected_pokemon


#use the saved pokemon as the dropdown value
if saved_pokemon in pokemon_options:
    st.session_state.index_pokemon_search = saved_pokemon

elif "index_pokemon_search" not in st.session_state:
    st.session_state.index_pokemon_search = "All Pokemon"


#save the pokemon when the dropdown changes
def save_pokemon():
    if st.session_state.index_pokemon_search != "All Pokemon":
        st.session_state.selected_pokemon = st.session_state.index_pokemon_search


#dropdown for searching pokemon
pokemon_search = st.selectbox(
    "Search by Pokemon Name",
    options=pokemon_options,
    key="index_pokemon_search",
    on_change=save_pokemon
)


#getting the types from the dataset
type_names = df['Type'].dropna() #remove missing values

all_types = []


#splitting the types for the ones with multiple types
for pokemon_type in type_names:

    #split the types
    for single_type in pokemon_type.split():

        #only add the type if it is not already in the list
        if single_type not in all_types:
            all_types.append(single_type)


#sort the types alphabetically
all_types = sorted(all_types)


#type and attack filters
filter_col1, filter_col2 = st.columns(2)

with filter_col1: #select a type, and the default option is "All Types"
    selected_type = st.selectbox("Choose Pokemon Type", options=["All Types"] + all_types)

with filter_col2: #slider for attack value, default is the minimum and maximum attack values in the dataset
    minimum_attack = st.slider("Minimum Attack Value", min_value=int(df['Attack'].min()), max_value=int(df['Attack'].max()), value=int(df['Attack'].min()))


#Filter the dataset
filtered = df.copy() #create a copy of the dataset to filter


#filter by name
if pokemon_search != "All Pokemon":
    filtered = filtered[filtered['Name'] == pokemon_search] #filter the dataset by selected pokemon


#filter by type
if selected_type != "All Types": #skipped if "All Types" is selected
    filtered = filtered[filtered['Type'].str.contains(selected_type, case=False, na=False, regex=False)] #filter the dataset by type, case insensitive, and ignore missing values


#filter by attack value
filtered = filtered[filtered['Attack'] >= minimum_attack] #filter the dataset by attack value


#sorting the results
st.header("Sorted Results")

sort_options = ["Pokedex Number", "Name", "Type", "Attack", "Defense", "HP"] #options for sorting

sort_option = st.selectbox("Sort By", options=sort_options) #dropdown for sorting options


#sort the filtered dataset
if sort_option == "Pokedex Number":
    filtered = filtered.sort_values("No")

elif sort_option == "Name":
    filtered = filtered.sort_values("Name")

elif sort_option == "Type":
    filtered = filtered.sort_values("Type")

elif sort_option == "Attack":
    filtered = filtered.sort_values("Attack", ascending=False)

elif sort_option == "Defense":
    filtered = filtered.sort_values("Defense", ascending=False)

elif sort_option == "HP":
    filtered = filtered.sort_values("HP", ascending=False)

st.divider()


#Display the results
st.header("Pokemon Search Results")


#check if the filtered dataset is empty
if filtered.empty:
    st.warning("No Pokemon found matching the search criteria.")

else:
    #how many results match the search criteria
    matching_pokemon = len(filtered)

    #calculate the average stats for the filtered pokemon
    average_hp = filtered['HP'].mean()
    average_attack = filtered['Attack'].mean()


    #display the metrics
    metric_columns = st.columns(3)

    with metric_columns[0]:
        st.metric("Pokemon Found", matching_pokemon)

    with metric_columns[1]:
        st.metric("Average HP", f"{average_hp:.2f}")

    with metric_columns[2]:
        st.metric("Average Attack", f"{average_attack:.2f}")


    #display the filtered dataset
    st.dataframe(filtered, use_container_width=True, hide_index=True)


#Pokemon Type Chart
st.divider()

st.header("Pokemon Type Comparison")

st.write("This chart shows the most common Pokemon types from your filtered results.")


#check if the filtered dataset is empty
if filtered.empty:
    st.info("Change your filters to see the Pokemon type chart.")

else:
    #count the pokemon types from the filtered dataset
    type_counts = filtered['Type'].value_counts() #count how many pokemon have each type or type combination

    #get the ten most common types
    top_types = type_counts.head(10)

    #display the bar chart
    st.bar_chart(top_types)
