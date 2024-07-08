import streamlit as st 
import pandas as pd
import numpy as np

from server_tools.Lyrics import Lyrics

# TODO: fix mistake in I Can Fix Him (No Really I Can) AND Mary's Song (Oh My My My)
all_lyrics = pd.read_csv("/home/jasmine/OneDrive - The University of Texas at Austin/Personal Projects/tayLyrics_v2/tayLyrics/TAYLOR_LYRICS_JUN2024.csv")
all_albums = ["Taylor Swift", 
              "Fearless (Taylor's Version)",
              "Speak Now (Taylor's Version)", 
              "Red (Taylor's Version)", 
              "1989 (Taylor's Version)", 
              "reputation", 
              "Lover", 
              "folklore", 
              "evermore", 
              "Midnights", 
              "THE TORTURED POETS DEPARTMENT"]
mode_options = ["Easy (an entire section, e.g. chorus)", 
                "Medium (2 lines)", 
                "Hard (1 line)"]
mode_mapping = {"Easy (an entire section, e.g. chorus)": "Easy", 
                "Medium (2 lines)": "Medium", 
                "Hard (1 line)": "Hard"}
points_mapping = {"Easy (an entire section, e.g. chorus)": 1, 
                 "Medium (2 lines)": 3, 
                 "Hard (1 line)": 5}
hint_help = """You get 3 hints per round; Hint 1 gives the album, 
               and Hint 2 and 3 give the next and previous line, 
               respectively. Each hint deducts 1 point from your total."""
gamemode_options = ["Casual (no lives)", 
                    "Survival (with 3 lives)"]

if "lyrics" not in st.session_state: 
    st.session_state.lyrics = Lyrics(data=all_lyrics)
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
if "hint_count" not in st.session_state: 
    st.session_state.hint_count = 0
if "guess" not in st.session_state: 
    st.session_state.guess = False
if "show_lyrics" not in st.session_state: 
    st.session_state.show_lyrics = False
if "disable_guess_input" not in st.session_state: 
    st.session_state.disable_guess_input = False
if "disable_giveup_btn" not in st.session_state: 
    st.session_state.disable_giveup_btn = False
if "next" not in st.session_state: 
    st.session_state.next = False
if "disable_hint_btn" not in st.session_state: 
    st.session_state.disable_hint_btn = False
if "round_count" not in st.session_state: 
    st.session_state.round_count = 0
if "points" not in st.session_state: 
    st.session_state.points = 0
if "disable_start_btn" not in st.session_state: 
    st.session_state.disable_start_btn = False
if "correct_rounds_count" not in st.session_state: 
    st.session_state.correct_rounds_count = 0

def guess_submitted():
    st.session_state.guess = st.session_state.widget
    st.session_state.widget = ""

# to be called when "Next Round" button is clicked
def new_round(mode): 
    st.session_state.hint_count = 0
    st.session_state.round_count += 1
    st.session_state.show_lyrics = True
    st.session_state.next = False
    st.session_state.disable_guess_input = False
    st.session_state.disable_hint_btn = False
    st.session_state.disable_giveup_btn = False

    generated_lyrics = st.session_state.lyrics.generate(mode)
    correct_song = st.session_state.lyrics.get_track_name()
    correct_album = st.session_state.lyrics.get_album_name()
    next_line = st.session_state.lyrics.get_next_line()
    prev_line = st.session_state.lyrics.get_previous_line()

    return generated_lyrics, correct_song, correct_album, next_line, prev_line

def end_current_game(): 
    st.session_state.disable_start_btn = False
    st.session_state.show_lyrics = False
    st.session_state.points = 0
    st.session_state.round_count = 0
    st.session_state.correct_rounds_count = 0

def disable_start_button(): 
    st.session_state.disable_start_btn = True

def next_round(): 
    st.session_state.next = True

def give_up(): 
    st.session_state.disable_guess_input = True
    st.session_state.points -= 2
    container.error(f"The correct answer was {st.session_state.correct_song}, from the album {st.session_state.correct_album}", icon="🚨")
    container.button("Next round", on_click=next_round)

def add_hint(): 
    st.session_state.hint_count += 1
    st.session_state.points -= 1
    if st.session_state.hint_count == 1: 
        container.info(f"Hint 1: this song comes from the album {st.session_state.correct_album}", icon="ℹ️")
    if st.session_state.hint_count == 2: 
        container.info(f'Hint 2: the next line of this song is "{st.session_state.next_line}"', icon="ℹ️")
    if st.session_state.hint_count == 3: 
        container.info(f'Hint 3: the previous line of this song is "{st.session_state.prev_line}"', icon="ℹ️")
        st.session_state.disable_hint_btn = True

def answered_correctly(): 
    container.success(f'That is correct! The answer is indeed {st.session_state.correct_song}, from the album {st.session_state.correct_album}. Well done!', icon="✅")
    st.session_state.points += points_mapping[mode]
    st.session_state.correct_rounds_count += 1
    st.session_state.guess = None
    st.session_state.disable_hint_btn = True
    st.session_state.disable_giveup_btn = True

    container.button("Next round", on_click=next_round)

def answered_incorrectly(): 
    container.error(f'"{st.session_state.guess}" is not correct. Please try again!', icon="🚨")
    st.session_state.points -= 1

# TODO: implement survival mode (w/ lives)

st.title("Welcome to :sparkles:tayLyrics:sparkles:!")

# SIDEBAR #
with st.sidebar: 
    with st.form("game_settings"): 
        mode = st.selectbox("Select a game difficulty", 
                            options=mode_options, 
                            disabled=st.session_state.disable_start_btn)
        game_mode = st.selectbox("Select a game mode", 
                                 options=gamemode_options,
                                 disabled=st.session_state.disable_start_btn)
        with st.expander("Advanced options"):
            selected_albums = st.multiselect("Select albums to generate lyrics from", 
                                             options=all_albums, 
                                             default=all_albums, 
                                             disabled=st.session_state.disable_start_btn)
        # TODO: disable button until game ends
        start_btn = st.form_submit_button("Start new game", disabled=st.session_state.disable_start_btn, on_click=disable_start_button)

# MAIN PANEL #
if (start_btn) or st.session_state.next: 
    st.session_state.generated_lyrics, st.session_state.correct_song, st.session_state.correct_album, st.session_state.next_line, st.session_state.prev_line = new_round(mode=mode)

container = st.container(border=True)
with container: 
    if st.session_state.show_lyrics:
        st.write(st.session_state.generated_lyrics, unsafe_allow_html=True)
        st.text_input("Enter your guess", 
                placeholder="e.g. Back to December or Shake it Off", 
                key="widget", on_change=guess_submitted,
                disabled=st.session_state.disable_guess_input)
        if st.session_state.guess: 
            if st.session_state.lyrics.get_guess_feedback(st.session_state.guess): 
                answered_correctly()
            else: 
                answered_incorrectly()
        col1, col2, col3, col4 = st.columns(4)
        hint_btn = col1.button("Hint", on_click=add_hint, disabled=st.session_state.disable_hint_btn, 
                               help=hint_help)
        giveup_btn = st.button("Give up", on_click=give_up, disabled=st.session_state.disable_giveup_btn,
                               help="2 points are deducted from your total if you give up.")
        col4.button("End current game", on_click=end_current_game)
    else: 
        st.markdown('Click the "Start new game" button to start guessing!')

st.sidebar.divider()
with st.sidebar.container(border=True):
    st.markdown("### Game Statistics")
    st.markdown(f"**{mode_mapping[mode]} difficulty, round {st.session_state.round_count}**")
    st.markdown(f"* Total points: {st.session_state.points}")
    if st.session_state.round_count: 
        accuracy_pct = round((st.session_state.correct_rounds_count / st.session_state.round_count), 2) * 100
        st.markdown(f"* Accuracy: {st.session_state.correct_rounds_count}/{st.session_state.round_count} ({accuracy_pct}%)")
        possible_pct = round((st.session_state.points / st.session_state.round_count * points_mapping[mode]), 2) * 100
        st.markdown(f"* :green[Points out of total possible: {st.session_state.points}/{st.session_state.round_count * points_mapping[mode]} ({possible_pct}%)]")
        