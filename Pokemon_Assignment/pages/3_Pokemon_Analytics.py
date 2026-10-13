
import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image 


#page configuration 
charzard_image = Image.open("Pokemon_Assignment/images/Pokémon_Charizard_art.png")
st.set_page_config(
    page_title = "Pokemon Analytics",
    page_icon = charzard_image,
    layout = "wide"
)


#cache the CSV 
@st.cache_data
def load_data():
    df = pd.read_csv("data/pokemon_data.csv")
    return df

df = load_data()


#session state
#checking for the pokemon from another page 
if "selected_pokemon" not in st.session_state:
    st.session_state.selected_pokemon = None


#page Header
logo_col, title_col = st.columns([1, 10])

with logo_col:
    st.image(charzard_image, width = 100)

with title_col:
    st.title("Pokemon Analytics")

st.write("Explore Pokemon Battle Statistics and compare types")

st.divider()


#Pokemon Card Type Graph
st.header("Pokemon Type Distribution")

st.write("This shows the ten most common Pokemon types in the data")

type_counts = df["Type"].value_counts().reset_index()

type_counts.columns = ["Type", "Count"]

top_types = type_counts.head(10)


#bar chart 
type_chart = px.bar(
    top_types,
    x = "Type",
    y = "Count",
    title = "Top 10 Pokemon Types",
    labels = {
        "Type": "Pokemon Type",
        "Count": "Number of Pokemon"
    }
)


#display barchart 
st.plotly_chart(type_chart, use_container_width = True)

st.divider()


#pokemon comparison chart
st.header("Pokemon Comparison")

st.write("Pick two pokemon to compare their battle stats")


#battle stats list
battle_stats = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]


#get the names from the set 
Pokemon_names = sorted(df["Name"].dropna().unique())


#get the saved pokemon
saved_pokemon = st.session_state.selected_pokemon


#saved pokemon as the first choice 
if saved_pokemon in Pokemon_names:
    default_index = Pokemon_names.index(saved_pokemon)

else:
    default_index = 0 


#start with a different pokemon for the second choice
second_index = 1 if default_index == 0 and len(Pokemon_names) > 1 else 0


#selecting the two pokemon 
compare_col1, compare_col2 = st.columns(2)

with compare_col1:

    #first pokemon
    pokemon_one = st.selectbox(
        "First Pokemon",
        options = Pokemon_names,
        index = default_index
    )

with compare_col2:

    #second pokemon dropdown 
    pokemon_two = st.selectbox(
        "Second Pokemon",
        options = Pokemon_names,
        index = second_index
    )


#if the same pokemon was picked 
if pokemon_one == pokemon_two:
    st.info("Pick another Pokemon")

else:

    #get first pokemon 
    pokemon_one_data = df[df["Name"] == pokemon_one].iloc[0]

    #get second pokemon 
    pokemon_two_data = df[df["Name"] == pokemon_two].iloc[0]


    #dataframe for comparison
    comparison_df = pd.DataFrame({
        "Stat": battle_stats,
        pokemon_one: [pokemon_one_data[stat] for stat in battle_stats],
        pokemon_two: [pokemon_two_data[stat] for stat in battle_stats]
    }) 


    #dataframe format for the chart 
    comparison_chart_data = comparison_df.melt(
        id_vars = "Stat",
        var_name = "Pokemon",
        value_name = "Value"
    )


    #bar chart 
    comparison_chart = px.bar(
        comparison_chart_data,
        x = "Stat",
        y = "Value",
        color = "Pokemon",
        barmode = "group",
        title = f"{pokemon_one} vs {pokemon_two}",
        labels = {
            "Stat": "Battle Stat",
            "Value": "Stat Value"
        }
    )


    #display comparison chart 
    st.plotly_chart(comparison_chart, use_container_width = True)

    st.dataframe(
        comparison_df,
        use_container_width = True, 
        hide_index = True
    )
