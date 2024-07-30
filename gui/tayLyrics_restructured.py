import streamlit as st
import pandas as pd

from servertools.Lyrics import Lyrics

### GLOBAL VARS ###
ALL_LYRICS = pd.read_csv("/home/jasmine/tayLyrics_v2/tayLyrics/TAYLOR_LYRICS_JUN2024.csv")
ALL_ALBUMS = ["Taylor Swift", 
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
DIFFICULTIES = ["Easy (an entire section, e.g. chorus)", 
                "Medium (2 lines)", 
                "Hard (1 line)"]
GAME_MODES = ["Casual (no lives)", 
              "Survival (with 3 lives)"]
POINTS_MAPPING = {"Easy (an entire section, e.g. chorus)": 1, 
                  "Medium (2 lines)": 3, 
                  "Hard (1 line)": 5}

### SESSION STATES ###
if "game_in_progress" not in st.session_state: 
    st.session_state.game_in_progress = False
if "lyrics" not in st.session_state: 
    st.session_state.lyrics = Lyrics(data=ALL_LYRICS)
if "generated_lyrics" not in st.session_state: 
    st.session_state.generated_lyrics = None
if "correct_song" not in st.session_state: 
    st.session_state.correct_song = None
if "correct_album" not in st.session_state: 
    st.session_state.correct_album = None
if "correct_section" not in st.session_state: 
    st.session_state.correct_section = None
if "next_line" not in st.session_state: 
    st.session_state.next_line = None
if "prev_line" not in st.session_state: 
    st.session_state.prev_line = None
if "round_count" not in st.session_state: 
    st.session_state.round_count = 0
if "guess" not in st.session_state:
    st.session_state.guess = None
if "disable_buttons" not in st.session_state: 
    st.session_state.disable_buttons = False
if "correct_feedback" not in st.session_state: 
    st.session_state.correct_feedback = None
if "incorrect_feedback" not in st.session_state: 
    st.session_state.incorrect_feedback = None
if "points" not in st.session_state: 
    st.session_state.points = 0
if "round_results" not in st.session_state:
    st.session_state.round_results = []
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "album_counter" not in st.session_state: 
    st.session_state.album_counter = {}

### FUNCTIONS ###
def clear_guess(): 
    """Clears the guess text input once an answer is submitted"""
    st.session_state.guess = st.session_state.temp_guess
    st.session_state.temp_guess = ""

def game_started(difficulty, game_mode, albums):
    st.session_state.game_in_progress = True
    st.session_state.correct_feedback = None
    st.session_state.difficulty = difficulty
    st.session_state.game_mode = game_mode
    st.session_state.albums = albums

    (st.session_state.generated_lyrics, 
     st.session_state.correct_song, 
     st.session_state.correct_album, 
     st.session_state.next_line, 
     st.session_state.prev_line, 
     st.session_state.correct_section) = new_round(difficulty)
    
    st.session_state.album_counter = {album_name: [] for album_name in st.session_state.albums}
    
def new_round(difficulty):
    st.session_state.round_count += 1

    generated_lyrics = f'<div class="lyrics">{st.session_state.lyrics.generate(difficulty)}</div>'
    correct_song = st.session_state.lyrics.get_track_name()
    correct_album = st.session_state.lyrics.get_album_name()
    next_line = st.session_state.lyrics.get_next_line()
    prev_line = st.session_state.lyrics.get_previous_line()
    section = st.session_state.lyrics.get_section()

    return generated_lyrics, correct_song, correct_album, next_line, prev_line, section

def answered_correctly():
    st.session_state.points += POINTS_MAPPING[st.session_state.difficulty]
    st.session_state.correct_feedback = f"""That is correct! The answer is indeed **{st.session_state.correct_song}**, 
                                            {st.session_state.correct_section}, from the album **{st.session_state.correct_album}**.
                                            \n\nYou earned {POINTS_MAPPING[st.session_state.difficulty]} points and have 
                                            {st.session_state.points} total points."""
    st.session_state.round_results.append(True)
    st.session_state.guess = None
    st.session_state.disable_buttons = True
    st.session_state.streak += 1
    st.session_state.album_counter[st.session_state.correct_album].append(True)

def answered_incorrectly():
    pass

### UI ###
if st.session_state.game_in_progress == False: 

    start_tab, leaderboard_tab = st.tabs(["Start New Game", "Leaderboard"])

    with start_tab: 
        with st.form("game_settings"):
            st.markdown("### Start a New Game")
            st.selectbox("Select a game difficulty", 
                         options=DIFFICULTIES,
                         key="difficulty")
            st.selectbox("Select a game mode",
                         options=GAME_MODES,
                         key="game_mode")
            with st.expander("Advanced options"):
                st.multiselect("Select albums to generate lyrics from",
                               options=ALL_ALBUMS,
                               default=ALL_ALBUMS,
                               key="albums")
            st.form_submit_button(":large_green_square: Start new game",
                                  on_click=game_started,
                                  kwargs=dict(difficulty=st.session_state.difficulty,
                                              game_mode=st.session_state.game_mode,
                                              albums=st.session_state.albums))
    with leaderboard_tab: 
        st.markdown("### Leaderboards")

else: 
    with st.container(border=True):
        st.write(f"<h4><u>Round {st.session_state.round_count}<u/></h4>", unsafe_allow_html=True)
        st.write(st.session_state.generated_lyrics, unsafe_allow_html=True)
        st.text("")
        st.text_input("Enter your guess",
                      placeholder="e.g. Back to December or Shake it Off",
                      key="temp_guess",
                      on_change=clear_guess,
                      disabled=st.session_state.disable_buttons)
        if st.session_state.guess: 
            if st.session_state.lyrics.get_guess_feedback(st.session_state.guess): 
                answered_correctly()
            else: 
                answered_incorrectly()
        
        if st.session_state.correct_feedback:
            st.success(f"{st.session_state.correct_feedback}", icon="✅")
            # next_rnd = st.button(":arrow_right: Next round",)#  on_click=new_round, args=(st.session_state.difficulty,))
            # if next_rnd: 
            #     new_round(st.session_state.difficulty)

print(f"difficulty {st.session_state.difficulty}")