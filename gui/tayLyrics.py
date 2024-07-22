import streamlit as st 
import pandas as pd
import numpy as np

from server_tools.Lyrics import Lyrics

# TODO: possibly add leaderboard? Only if all albums selected

# TODO: fix mistake in I Can Fix Him (No Really I Can) AND Mary's Song (Oh My My My)
all_lyrics = pd.read_csv("/home/jasmine/tayLyrics_v2/tayLyrics/TAYLOR_LYRICS_JUN2024.csv")
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
if "lives" not in st.session_state: 
    st.session_state.lives = 3
if "past_game_scores" not in st.session_state:
    st.session_state.past_game_scores = None
if "streak" not in st.session_state: 
    st.session_state.streak = 0
if "streaks" not in st.session_state: 
    st.session_state.streaks = []
if "disable_general" not in st.session_state: 
    st.session_state.disable_general = False


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
    accuracy_pct = round((st.session_state.correct_rounds_count / st.session_state.round_count), 2) * 100
    possible_pct = (st.session_state.points / (st.session_state.round_count * points_mapping[mode])) * 100

    st.session_state.past_game_scores = f"""
**{mode_mapping[mode]} difficulty, {st.session_state.round_count} rounds played**
* :dart: Accuracy: {st.session_state.correct_rounds_count}/{st.session_state.round_count} ({accuracy_pct}%)
* :100: Points out of total possible: {st.session_state.points}/{st.session_state.round_count * points_mapping[mode]} ({round(possible_pct, 2)}%)
* :fire: Max streak: {max(st.session_state.streaks) if len(st.session_state.streaks) else 0}
* :moneybag: :green[**Total points: {st.session_state.points}**]
"""

    st.session_state.streak = 0
    st.session_state.streaks = []
    st.session_state.disable_start_btn = False
    st.session_state.disable_general = False
    st.session_state.show_lyrics = False
    st.session_state.points = 0
    st.session_state.round_count = 0
    st.session_state.correct_rounds_count = 0

def disable_start_button(): 

    if len(st.session_state.albums) == 0: 
        start_form.error("Please select at least one album.")
    else: 
        st.session_state.disable_start_btn = True
        st.session_state.disable_general = True
        st.session_state.lives = 3

        filtered_lyrics = all_lyrics[all_lyrics["album_name"].isin(st.session_state.albums)].reset_index()
        st.session_state.lyrics = Lyrics(data=filtered_lyrics)
    

def next_round(): 
    st.session_state.next = True

def give_up(game_mode): 
    st.session_state.disable_guess_input = True
    st.session_state.disable_giveup_btn = True
    st.session_state.disable_hint_btn = True
    st.session_state.points -= 2
    st.session_state.lives -= 1
    st.session_state.streaks.append(st.session_state.streak)
    st.session_state.streak = 0
    msg = f"The correct answer was {st.session_state.correct_song}, from the album {st.session_state.correct_album}"        
    if game_mode == "Survival (with 3 lives)":
        msg = f"The correct answer was {st.session_state.correct_song}, from the album {st.session_state.correct_album}. \n\nYou lost a life and have {st.session_state.lives} lives left."
        if st.session_state.lives == 0: 
            container.error(f"**GAME OVER**: You ran out of lives! Please start a new game.", icon="😢")
            # TODO: print correct answer befre ending game
            container.error(msg, icon="🚨")
            end_current_game()
            return
    # TODO: it is showing the error twice - this stuff down here runs even if game over
    container.error(msg, icon="🚨")
    container.button(":arrow_right: Next round", on_click=next_round)

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
    st.session_state.streak += 1

    container.button(":arrow_right: Next round", on_click=next_round)

def answered_incorrectly(game_mode): 
    msg = f'"{st.session_state.guess}" is not correct. Please try again!'
    st.session_state.points -= 1
    st.session_state.lives -= 1
    st.session_state.streaks.append(st.session_state.streak)
    st.session_state.streak = 0
    if game_mode == "Survival (with 3 lives)":
        msg = msg + f"\n\nYou lost a life and have {st.session_state.lives} lives left."
        if st.session_state.lives == 0: 
            container.error(f"**GAME OVER**: You ran out of lives! Please start a new game.", icon="😢")
            # TODO: print correct answer befre ending game
            container.error(f"The correct answer was {st.session_state.correct_song}, from the album {st.session_state.correct_album}", icon="🚨")
            end_current_game()
    container.error(msg, icon="🚨")
    

st.title("Welcome to :sparkles:tayLyrics:sparkles:!")

# SIDEBAR #
sidebar = st.sidebar
with sidebar: 
    with st.expander(":pencil2: Instructions"): 
        st.markdown(f"Lyrics range from debut to *{all_albums[-1]}*.")
        st.markdown(f':red[**IMPORTANT: do NOT include parentheses in your guesses; e.g. "Back to December (Taylor\'s Version)" should simply be "Back to December."**]')
    start_form = st.form("game_settings")
    with start_form:
        mode = st.selectbox("Select a game difficulty", 
                            options=mode_options, 
                            disabled=st.session_state.disable_general)
        game_mode = st.selectbox("Select a game mode", 
                                 options=gamemode_options,
                                 disabled=st.session_state.disable_general)
        with st.expander("Advanced options"):
            selected_albums = st.multiselect("Select albums to generate lyrics from", 
                                             options=all_albums, 
                                             default=all_albums, 
                                             disabled=st.session_state.disable_general, 
                                             # on_change=albums_selected, 
                                             key="albums")
        start_btn = st.form_submit_button(":large_green_square: Start new game", disabled=(st.session_state.disable_start_btn),
                                          on_click=disable_start_button)

# MAIN PANEL #
if (start_btn and len(selected_albums)) or st.session_state.next: 
    st.session_state.generated_lyrics, st.session_state.correct_song, st.session_state.correct_album, st.session_state.next_line, st.session_state.prev_line = new_round(mode=mode)
    st.write(st.session_state.lyrics.rand_num)

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
                answered_incorrectly(game_mode=game_mode)
        col1, col2, col3 = st.columns(3)
        hint_btn = col1.button(":bulb: Hint", on_click=add_hint, disabled=st.session_state.disable_hint_btn, 
                               help=hint_help)
        giveup_btn = st.button(":no_entry: Give up", on_click=give_up, disabled=st.session_state.disable_giveup_btn,
                               help="2 points are deducted from your total if you give up.", args=(game_mode,))
        col3.button(":octagonal_sign: End current game", on_click=end_current_game)
    else: 
        st.markdown('Click the "Start new game" button to start guessing!')
        if st.session_state.past_game_scores: 
            st.markdown("### Past Game Statistics")
            st.markdown(st.session_state.past_game_scores)

st.sidebar.divider()
with st.sidebar.container(border=True):
    st.markdown("### Game Statistics")
    # TODO: add the album filtering stuff; all if all, otherwise list all
    st.markdown(f"**{mode_mapping[mode]} difficulty, {game_mode} mode**")
    if st.session_state.round_count: 
        st.markdown(f"* :large_green_circle: **Round: {st.session_state.round_count}**")
        accuracy_pct = round((st.session_state.correct_rounds_count / st.session_state.round_count), 2) * 100
        st.markdown(f"* :dart: Accuracy: {st.session_state.correct_rounds_count}/{st.session_state.round_count} ({accuracy_pct}%)")
        possible_pct = (st.session_state.points / (st.session_state.round_count * points_mapping[mode])) * 100
        st.markdown(f"* :100: Points out of total possible: {st.session_state.points}/{st.session_state.round_count * points_mapping[mode]} ({round(possible_pct, 2)}%)")
        st.markdown(f"* :fire: Current streak: {st.session_state.streak}")
        st.markdown(f"* :moneybag: :green[**Total points: {st.session_state.points}**]")
    if game_mode == "Survival (with 3 lives)":
        st.markdown(f"* :red[Lives: {st.session_state.lives}]")