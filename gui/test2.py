import streamlit as st 
import pandas as pd
import numpy as np
import random

from server_tools.Lyrics import Lyrics

all_lyrics = pd.read_csv("/home/jasmine/OneDrive - The University of Texas at Austin/Personal Projects/tayLyrics_v2/tayLyrics/TAYLOR_LYRICS_JUN2024.csv")
all_albums = np.unique(all_lyrics["album_name"])
mode_options = ["Easy (an entire section, e.g. chorus)", 
                "Medium (2 lines)", 
                "Hard (1 line)"]

if "lyrics" not in st.session_state: 
    st.session_state.lyrics = Lyrics(data=all_lyrics)
if "guess" not in st.session_state: 
    st.session_state.guess = None
if "generate_btn_state" not in st.session_state: 
    st.session_state.generate_btn_state = False
if "generated_lyrics" not in st.session_state: 
    st.session_state.generated_lyrics = None
if "correct_song" not in st.session_state: 
    st.session_state.correct_song = None
if "correct_album" not in st.session_state: 
    st.session_state.correct_album = None
if "next_line" not in st.session_state: 
    st.session_state.next_line = None
if "prev_line" not in st.session_state: 
    st.session_state.prev_line = None
# if 'button_clicked' not in st.session_state:
#     st.session_state.button_clicked = False
if "next" not in st.session_state: 
    st.session_state.next = False
if "hint_count" not in st.session_state: 
    st.session_state.hint_count = 0


def submit():
    st.session_state.guess = st.session_state.widget
    st.session_state.widget = ""

def next_round(): 
    st.session_state.next = True

def disable_btn(): 
    st.session_state.button_clicked = True

def round(mode): 
    generated_lyrics = st.session_state.lyrics.generate(mode)
    correct_song = st.session_state.lyrics.get_track_name()
    correct_album = st.session_state.lyrics.get_album_name()
    next_line = st.session_state.lyrics.get_next_line()
    prev_line = st.session_state.lyrics.get_previous_line()
    return generated_lyrics, correct_song, correct_album, next_line, prev_line

def add_hint(): 
    st.session_state.hint_count += 1

def give_up(): 
    st.error(f"The correct answer was {st.session_state.correct_song}, from the album {st.session_state.correct_album}", icon="🚨")
    next_round()

# TODO: implement survival mode (w/ lives)

st.title("Welcome to :sparkles:tayLyrics:sparkles:!")

# SIDEBAR #
with st.sidebar: 
    with st.form("game_settings"): 
        mode = st.selectbox("Select a game mode", 
                            options=mode_options)
        with st.expander("Advanced options"):
            selected_albums = st.multiselect("Select albums to generate lyrics from", 
                                             options=all_albums, 
                                             default=all_albums)
        start_btn = st.form_submit_button("Start game")

# MAIN PANEL #

generated_lyrics = None
hint_btn = False
if (start_btn) or (st.session_state.next):
    st.session_state.generate_btn_state = True
    st.session_state.next = False
    st.session_state.generated_lyrics, st.session_state.correct_song, st.session_state.correct_album, st.session_state.next_line, st.session_state.prev_line = round(mode=mode)
with st.container(border=True): 
    if st.session_state.generate_btn_state:
        st.write(st.session_state.generated_lyrics, unsafe_allow_html=True)
        st.text_input("Enter your guess", 
                      placeholder="e.g. Back to December or Shake it Off", 
                      key="widget", on_change=submit)
        hint_btn = st.button("Hint", on_click=add_hint)
        giveup_btn = st.button("Give up", on_click=give_up)
    if st.session_state.hint_count == 1: 
        st.info(f"Hint 1: this song comes from the album {st.session_state.correct_album}", icon="ℹ️")
    if st.session_state.hint_count == 2: 
        st.info(f"Hint 2: the next line of this song is {st.session_state.next_line}", icon="ℹ️")
    if st.session_state.hint_count == 3: 
        st.info(f"Hint 3: the previous line of this song is {st.session_state.prev_line}", icon="ℹ️")
    if st.session_state.guess: 
        if st.session_state.lyrics.get_guess_feedback(st.session_state.guess): 
            st.session_state.button_clicked = False
            st.success(f'That is correct! The answer is indeed {st.session_state.correct_song}, from the album {st.session_state.correct_album}. Well done!', icon="✅")
            st.session_state.guess = None
            st.button("Next round", key="next_btn", on_click=next_round)
        else: 
            st.error(f'"{st.session_state.guess}" is not correct. Please try again!', icon="🚨")

st.write(st.session_state.correct_song)
st.write(st.session_state.guess)
st.write(f"next: {st.session_state.next}")
