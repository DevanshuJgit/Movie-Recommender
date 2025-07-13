import streamlit as st
import pickle
import pandas as pd
import requests

movies_list = pickle.load(open('movies.pkl', 'rb'))
sim = pickle.load(open('sim.pkl', 'rb'))
movies = pd.DataFrame(movies_list)

def fetch_poster(movie_id):
    headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxYzBjZDgzOTc0MWRlOWQ2YzM4YmZkZTZkZmEyMjIxMyIsIm5iZiI6MTc1MDUxNTE2OC4xOTkwMDAxLCJzdWIiOiI2ODU2YmRlMDY3MDc3YmJlY2VjYjRhZmMiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.yJ9qUWjNfY24vgsSn-AZcgKY1JfKbfiwrNeIvvC25QQ"
    }
    response = requests.get('https://api.themoviedb.org/3/movie/{}?language=en-US'.format(movie_id), headers=headers)
    data = response.json()
    return "http://image.tmdb.org/t/p/w500/"+data['poster_path']

def recommend(movie):
    movie_index = movies[movies['original_title']==movie].index[0]
    d = sim[movie_index]
    movies_list = sorted(list(enumerate(d)), reverse=True, key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].original_title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

st.title("Movie Recommender System")

selected_name = st.selectbox(
    "Select Movie Name For Recommendation",
    movies['original_title'].values
)

if st.button('Recommend'):
    name, poster = recommend(selected_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(name[0])
        st.image(poster[0])
    with col2:
        st.text(name[1])
        st.image(poster[1])
    with col3:
        st.text(name[2])
        st.image(poster[2])
    with col4:
        st.text(name[3])
        st.image(poster[3])
    with col5:
        st.text(name[4])
        st.image(poster[4])
    
