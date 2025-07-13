import pandas as pd
import numpy as np
import streamlit as st
import pickle as pkl

# Load data
df = pd.read_csv("cleaned_data.csv")
movies = sorted(df["title"])
similarity = pkl.load(open("similarity.pkl", "rb"))

# Inject Custom Advanced CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Montserrat', sans-serif;
        background: linear-gradient(to bottom right, #0f0c29, #302b63, #24243e);
        color: white;
    }

    .main-title {
        font-size: 3.2rem;
        text-align: center;
        padding: 20px;
        color: #ff4e50;
        background: -webkit-linear-gradient(left, #ff4e50, #f9d423);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glow 2s infinite alternate;
    }

    @keyframes glow {
        from { text-shadow: 0 0 10px #f9d423; }
        to { text-shadow: 0 0 20px #ff4e50; }
    }

    .stButton > button {
        background-color: #ff4e50;
        color: white;
        border: none;
        border-radius: 30px;
        padding: 10px 25px;
        font-size: 1rem;
        transition: 0.4s;
        margin-top: 20px;
    }

    .stButton > button:hover {
        background-color: #f9d423;
        color: black;
        transform: scale(1.05);
    }

    .recommend-box {
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 20px;
        padding: 20px;
        margin: 20px auto;
        width: 90%;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(10px);
        font-size: 1.1rem;
        animation: popin 0.5s ease-in-out;
    }

    @keyframes popin {
        from { opacity: 0; transform: scale(0.95); }
        to { opacity: 1; transform: scale(1); }
    }

    .error-msg {
        font-size: 1.3rem;
        color: #ff4e50;
        text-align: center;
        padding: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎬 Movie Recommendation Engine</div>', unsafe_allow_html=True)

# Functions
def get_movie_title(index):
    if len(df) > index:
        return df.loc[index, "title"]
    return ''

def get_movie_index(title):
    for i in range(len(df)):
        if df.loc[i, "title"].lower() == title.lower():
            return i
    return -1

# Input
title = st.selectbox("🎥 Choose a Movie You Like:", movies)

if st.button("🔥 Get Me Recommendations!"):
    index = get_movie_index(title)
    if index == -1:
        st.markdown('<div class="error-msg">❌ Movie not found. Try a different title!</div>', unsafe_allow_html=True)
    else:
        sorted_indices = np.argsort(-similarity[index])
        st.markdown(f'<div class="recommend-box">✨ Top 5 Movies Similar to <b>{title}</b>:</div>', unsafe_allow_html=True)
        for i in range(1, 6):
            rec_title = get_movie_title(sorted_indices[i])
            st.markdown(f'<div class="recommend-box">🎞️ {i}. {rec_title}</div>', unsafe_allow_html=True)
