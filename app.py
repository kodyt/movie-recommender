import streamlit as st
import pickle
import pandas as pd
import requests
from random import randrange

# API Key = a21cb99f37a0def5d34b4899100a858f
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=a21cb99f37a0def5d34b4899100a858f&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/original" + data['poster_path']
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies = []
    posters = []
    for val in movies_list:
        movie_id = movies.iloc[val[0]].movie_id
        
        recommended_movies.append(movies.iloc[val[0]].title)
        
        # Fetch the poster from api
        posters.append(fetch_poster(movie_id))
        # print(new_df.iloc[movie[0]].title)
    return recommended_movies, posters

def random():
    id = randrange(len(movies))
    movie_id = movies.iloc[id].movie_id
    poster = fetch_poster(movie_id)
    return movies.iloc[id].title, poster



movies_dict = pickle.load(open("movie_dict.pkl", 'rb'))
movies = pd.DataFrame(movies_dict)


similarity = pickle.load(open("similarity.pkl", 'rb'))



################################################################
st.title("Kody's Movie Recommender")

selected_movie_name = st.selectbox(
    'Pick a movie to find similar ones!', movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    # for rec in recommendations:
    #     st.write(rec)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])

if st.button('Random Movie'):
    name, poster = random()
    st.text(name)
    st.image(poster, width=150)
    # st.markdown("[![Foo]({})]({})".format(poster, link), width=150)


