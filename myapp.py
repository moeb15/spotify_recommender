import pandas as pd
import streamlit as st
import joblib
from kmodes.kmodes import KModes
from utils.recommender_utils import recommend_artists

kmodes_model, encoder = joblib.load('models/model.pkl') 
transactional_data = pd.read_csv('data/transactional_data.csv')
tabular_data = pd.read_csv('data/ag_data.csv')

genres = list(set(tabular_data['Subgenre'].tolist()))


def main_app():
    st.write("""
    ## Spotify Artists Recommendations
    Select your favourite genres and in return get artists recommendeded to you!
    Re-enter your selection to get another batch of artists recommended to you.
    """)

    selected_genres = st.multiselect(label='Choose your favourite genres',options=genres)
    num_artists = st.slider("Number of artists",5,20,1)
    recommendations = recommend_artists(selected_genres,kmodes_model,encoder,transactional_data,num_artists)

    rec_str = ''

    for artist in recommendations:
        rec_str += "- " + artist + "\n"

    st.markdown(rec_str)


if __name__ == "__main__":
    main_app()