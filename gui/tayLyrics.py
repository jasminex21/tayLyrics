import streamlit as st 
import pandas as pd
import numpy as np
import random

from server_tools.generate_lyric import generate_lyric
# from server_tools.Lyrics import Lyrics

all_lyrics = pd.read_csv("/home/jasmine/OneDrive - The University of Texas at Austin/Personal Projects/tayLyrics_v2/tayLyrics/TAYLOR_LYRICS_JUN2024.csv")
all_albums = np.unique(all_lyrics["album_name"])
mode_options = ["Easy (an entire section, e.g. chorus)", 
                "Medium (2 lines)", 
                "Hard (1 line)"]

if "generate_btn_clicked" not in st.session_state:
    st.session_state.generate_btn_clicked = False

def click_button():
    st.session_state.generate_btn_clicked = not st.session_state.generate_btn_clicked

st.title("Welcome to :sparkles:tayLyrics:sparkles:!")

# SIDEBAR #
with st.sidebar: 
    st.subheader("How to play:guitar:")

# MAIN PANEL #
col1, buffer, col2 = st.columns([3, 1, 2])
with col1: 
    mode = st.selectbox("Select a game mode", 
                        options=mode_options)
with st.expander("Advanced options"):
    selected_albums = st.multiselect("Select albums to generate lyrics from", 
                                    options=all_albums, 
                                    default=all_albums)
    # TODO: set seed option

generate_btn = st.button("Generate")
if generate_btn: 
    with st.container(border=True): 
        generated_lyrics = generate_lyric(all_lyrics, mode=mode)
        st.write(generated_lyrics, unsafe_allow_html=True)