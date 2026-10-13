
import streamlit as st
import pandas as pd
import requests
from PIL import Image


#page configuration
charzard_image = Image.open("images/Pokémon_Charizard_art.png")

st.set_page_config(
    page_title = "Pokemon TCG",
    page_icon = charzard_image,
    layout = "wide"
)


#load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/pokemon_data.csv")
    return df

df = load_data()


#session state
if "selected_pokemon" not in st.session_state:
    st.session_state.selected_pokemon = None


#Page Header
logo_col, title_col = st.columns([1, 10])

with logo_col:
    st.image(charzard_image, width = 100)

with title_col:
    st.title("Pokemon TCG")

st.write("Search the Trading Cards, View their artwork, and Explore the market")

st.divider()


#Api functions
api_url = "https://api.tcgdex.net/v2/en/cards" #tcgdex api endpoint for searching cards


#storing the results
@st.cache_data(ttl=3600)
def search_cards(pokemon_name):

    #the api uses the "name" parameter to search for cards
    params = {
        "name": pokemon_name,
        "pagination:page": 1,
        "pagination:itemsPerPage": 20
    }

    #send the request to the API
    response = requests.get(
        api_url,
        params = params,
        timeout = 10
    )

    #check for error
    response.raise_for_status()

    #json into python
    data = response.json()

    #convert the list of cards into the pandas dataframe
    cards_df = pd.DataFrame(data)

    return cards_df


#this end point returns additional information (Search was for basic info)
@st.cache_data(ttl = 3600)
def get_card_details(card_id):

    #use the selected cards id to build the url
    detail_url = f"{api_url}/{card_id}"

    #request detailed card information
    response = requests.get(detail_url, timeout = 10)

    #check for errors
    response.raise_for_status()

    #convert the response from JSON into a dictionary
    card_details = response.json()

    return card_details


#Search for Trading Cards
st.header("Search Pokemon Cards")


#get the saved pokemon from the other pages
saved_pokemon = st.session_state.selected_pokemon


#uses the saved pokemon as the starting search
#if there's no search then empty box
if saved_pokemon is None:
    default_search = ""

else:
    default_search = saved_pokemon


#keep the search box updated with the saved pokemon
if "tcg_last_saved_pokemon" not in st.session_state:
    st.session_state.tcg_last_saved_pokemon = saved_pokemon

    if "tcg_pokemon_search" not in st.session_state:
        st.session_state.tcg_pokemon_search = default_search


#update the search if another page changed the pokemon
if st.session_state.tcg_last_saved_pokemon != saved_pokemon:
    st.session_state.tcg_pokemon_search = default_search
    st.session_state.tcg_last_saved_pokemon = saved_pokemon


#search box
#keep the saved or type a new name
pokemon_search = st.text_input(
    "Pokemon Name:",
    key = "tcg_pokemon_search",
    placeholder = "Example: Pikachu"
)


#button for the search
search_button = st.button("Search Cards")


#run when clicked
if search_button:

    #Check for user entry
    if pokemon_search.strip() == "":
        st.warning("Please Type A Name")

    else:
        #spinner while loading
        with st.spinner("Searching for Pokemon Cards..."):

            #searching for cards using the api
            try:
                cards_df = search_cards(pokemon_search.strip())

                #save the results in the session state
                st.session_state.tcg_results = cards_df

                #remember the results to the name
                st.session_state.tcg_search_name = pokemon_search.strip()


                #check if the searched pokemon is in the dataset
                matching_pokemon = df[
                    df["Name"].str.lower() == pokemon_search.strip().lower()
                ]


                #save the searched pokemon for the other pages
                if not matching_pokemon.empty:
                    st.session_state.selected_pokemon = matching_pokemon.iloc[0]["Name"]

                    #remember which pokemon was last saved
                    st.session_state.tcg_last_saved_pokemon = st.session_state.selected_pokemon


            #catch connection errors
            except requests.exceptions.RequestException:
                st.error(
                    "Could not connect, Please try again."
                )

                st.session_state.tcg_results = pd.DataFrame()

            #catching invalid JSON responses
            except ValueError:
                st.error("The API returned an invalid response.")

                st.session_state.tcg_results = pd.DataFrame()


#Display the search results
#check whether the user has already searched
if "tcg_results" not in st.session_state:

    st.info("Enter a Pokemon name and click Search Cards")

else:
    #get the saved result
    cards_df = st.session_state.tcg_results

    #check if the API returned matching cards
    if cards_df.empty:
        st.warning("No Trading Cards found for this search")

    else:
        st.divider()

        st.header("Trading Card Results")

        #number of cards returned
        total_cards = len(cards_df)

        #display number of returned cards
        st.metric("Cards Returned", total_cards)

        #show API search Response in the form of a table
        st.dataframe(
            cards_df[["id", "name", "localId"]],
            use_container_width = True,
            hide_index = True
        )


        #select a trading Card
        st.header("Select a Trading Card")

        st.write("Choose a card to view its information")

        #list of card ID's
        card_ids = cards_df["id"].tolist()

        #dropdown with the ID's
        selected_card = st.selectbox("Choose A Card", options = card_ids)


        #get card details
        #requests details for the chosen card
        try:
            card = get_card_details(selected_card)

        except requests.exceptions.RequestException:
            st.error("Could Not Load The Selected Card")

            st.stop()

        except ValueError:
            st.error("The API returned invalid card details")

            st.stop()


        st.divider()


        #Display card information
        st.header("Card Details")

        image_col, info_col = st.columns(2)


        #display card image
        with image_col:

            #image url from api
            image_url = card.get("image")

            #/high.webp to request the high resolution image
            if image_url:
                st.image(
                    image_url + "/high.webp",
                    width = 300
                )

            else:
                st.info("No image available for this card")


        #display card information
        with info_col:

            #get the value from the dictionary
            card_name = card.get("name", "Unknown")
            card_id = card.get("id", "Unknown")
            rarity = card.get("rarity", "Not Available")
            hp = card.get("hp", "Not Available")

            # The set information is stored in another dictionary.
            card_set = card.get("set") or {}

            set_name = card_set.get("name", "Not Available")

            st.subheader(card_name)

            st.write(f"**Card ID:** {card_id}")
            st.write(f"**Set:** {set_name}")
            st.write(f"**Rarity:** {rarity}")
            st.write(f"**HP:** {hp}")


        st.divider()

        st.header("Card Market Prices")

        st.write("The Prices are in USD from TCGPlayer")


        #price info for pricing section
        pricing = card.get("pricing") or {}

        #getting the pricing information from tcg
        tcgplayer = pricing.get("tcgplayer") or {}


        #Checking if the TCGplayer pricing data exists
        if not tcgplayer:

            st.info(
                "No TCGplayer pricing information available for this card"
            )

        else:
            #there are different prices for variations of the cards
            #list for available prices
            price_rows = []


            #API going through each price
            for variant_name, variant_data in tcgplayer.items():

                #only process the prices, exclude other values
                if isinstance(variant_data, dict):

                    market_price = variant_data.get("marketPrice")

                    low_price = variant_data.get("lowPrice")

                    #add the variant if at least one price exists
                    if market_price is not None or low_price is not None:
                        price_rows.append(
                            {
                                "Variant": variant_name,
                                "Market Price (USD)": market_price,
                                "Low Price (USD)": low_price
                            }
                        )


            #Check for any price at all
            if len(price_rows) == 0:

                st.info("No Market Price Available")

            else:
                #convert the prices into the data frame
                prices_df = pd.DataFrame(price_rows)

                #display the prices in a table
                st.dataframe(
                    prices_df,
                    use_container_width = True,
                    hide_index = True
                )
