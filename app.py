import streamlit as st
import pickle
import pandas as pd
import requests
from PIL import Image

# styling of the web pages
# Page title of the website i.e. MyRecpmmender
img = Image.open('images/image.jpg')
st.set_page_config(page_title='MyRecommender', page_icon=img, layout="wide")

# MAIN TITLE OF WEB PAGE
st.markdown(
    "<h1 "
    "style = 'text-align: center;" "color: white;' >MOVIE RECOMMENDER SYSTEM</h1>"
    , unsafe_allow_html=True
)

# for hiding the footer and main menu of the website
hide_menu_style = """
    <style>
     MainMenu {visibility : hidden;}
     footer {visibility : hidden;}
    </style> 
     """
st.markdown(hide_menu_style, unsafe_allow_html=True)


# fetching data from the api and also from the model
# for fetching poster path from the api
# website tmdb movie
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=d368413c1d7d89c26c98239003ffa0fb&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


# main function of the website for recommending movies
def recommend(movie, no_of_movies_recommended):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])

    recommended_movies_names = []
    recommended_movies_posters = []
    for i in movies_list[:no_of_movies_recommended]:
        movie_id = movies.iloc[i[0]].movie_id

        # fetch posters from api
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies_names.append(movies.iloc[i[0]].title)

    return recommended_movies_names, recommended_movies_posters


pickles_dir = "pkls"
# for getting data i.e. our movies dataframe ->pickle is used
movies_dict = pickle.load(open(f'{pickles_dir}/movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open(f'{pickles_dir}/similarity.pkl', 'rb'))

# subtitle for the dropdown menu
movie_list = movies['title'].values
selected_movie_name = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# after clicking on the recommend button main function
if st.button('Recommend'):
    no_of_movies_recommended = 8
    recommended_movies_names, recommended_movies_posters = recommend(selected_movie_name, no_of_movies_recommended)
    col = st.columns(no_of_movies_recommended)
    for idx in range(no_of_movies_recommended):
        with col[idx]:
            st.text(recommended_movies_names[idx])
            st.image(recommended_movies_posters[idx])
