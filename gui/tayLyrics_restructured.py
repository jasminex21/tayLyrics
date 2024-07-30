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
GAME_MODES = ["Survival (with 3 lives)",
              "Casual (no lives)"]
POINTS_MAPPING = {"Easy (an entire section, e.g. chorus)": 1, 
                  "Medium (2 lines)": 3, 
                  "Hard (1 line)": 5}
DIFFICULTY_MAPPING = {"Easy (an entire section, e.g. chorus)": "Easy", 
                      "Medium (2 lines)": "Medium", 
                      "Hard (1 line)": "Hard"}

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
    st.session_state.round_count = 1
if "guess" not in st.session_state:
    st.session_state.guess = None
if "disable_buttons" not in st.session_state: 
    st.session_state.disable_buttons = False
if "correct_feedback" not in st.session_state: 
    st.session_state.correct_feedback = ""
if "incorrect_feedback" not in st.session_state: 
    st.session_state.incorrect_feedback = ""
if "points" not in st.session_state: 
    st.session_state.points = 0
if "round_results" not in st.session_state:
    st.session_state.round_results = []
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "streaks" not in st.session_state:
    st.session_state.streaks = []
if "album_counter" not in st.session_state: 
    st.session_state.album_counter = {}
if "difficulty" not in st.session_state:
    st.session_state.difficulty = None
if "game_mode" not in st.session_state:
    st.session_state.game_mode = None
if "albums" not in st.session_state:
    st.session_state.albums = []
if "lives" not in st.session_state:
    st.session_state.lives = 3
if "hints" not in st.session_state:
    st.session_state.hints = 0
if "hints_used" not in st.session_state:
    st.session_state.hints_used = 0
if "gameover_feedback" not in st.session_state:
    st.session_state.gameover_feedback = ""
if "disable_hint_btn" not in st.session_state:
    st.session_state.disable_hint_btn = False
if "hint_feedback" not in st.session_state:
    st.session_state.hint_feedback = ""
if "giveup_feedback" not in st.session_state:
    st.session_state.giveup_feedback = ""
if "album_accs" not in st.session_state:
    st.session_state.album_accs = {}
if "past_game_stats" not in st.session_state:
    st.session_state.past_game_stats = ""

### FUNCTIONS ###
def clear_guess(): 
    """Clears the guess text input once an answer is submitted"""
    st.session_state.guess = st.session_state.temp_guess
    st.session_state.temp_guess = ""

def game_started(difficulty, game_mode, albums):
    st.session_state.game_in_progress = True
    st.session_state.correct_feedback = ""
    st.session_state.incorrect_feedback = ""
    st.session_state.gameover_feedback = ""
    st.session_state.hint_feedback = ""

    st.session_state.difficulty = difficulty
    st.session_state.game_mode = game_mode
    st.session_state.albums = albums

    (st.session_state.generated_lyrics, 
     st.session_state.correct_song, 
     st.session_state.correct_album, 
     st.session_state.next_line, 
     st.session_state.prev_line, 
     st.session_state.correct_section) = regenerate()
    
    st.session_state.album_counter = {album_name: [] for album_name in st.session_state.albums}
    
def new_round():
    st.session_state.round_count += 1
    st.session_state.disable_buttons = False
    st.session_state.disable_hint_btn = False
    st.session_state.correct_feedback = ""
    st.session_state.incorrect_feedback = ""
    st.session_state.giveup_feedback = ""

    (st.session_state.generated_lyrics, 
     st.session_state.correct_song, 
     st.session_state.correct_album, 
     st.session_state.next_line, 
     st.session_state.prev_line, 
     st.session_state.correct_section) = regenerate()

def regenerate():
    generated_lyrics = f'<div class="lyrics">{st.session_state.lyrics.generate(st.session_state.difficulty)}</div>'
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
    st.session_state.disable_hint_btn = True
    st.session_state.streak += 1
    st.session_state.album_counter[st.session_state.correct_album].append(True)

def answered_incorrectly():
    st.session_state.points -= 1
    st.session_state.incorrect_feedback = f'''"{st.session_state.guess}" is not correct. Please try again!\n\nYou lost 1 point and have {st.session_state.points} total points.'''
    st.session_state.lives -= 1
    st.session_state.streaks.append(st.session_state.streak)
    st.session_state.streak = 0

    if st.session_state.game_mode == "Survival (with 3 lives)":
        st.session_state.incorrect_feedback += f"\n\nYou lost a life and have {st.session_state.lives} lives left."
        if st.session_state.lives == 0:
            st.session_state.disable_buttons = True
            st.session_state.round_results.append(False)
            st.session_state.album_counter[st.session_state.correct_album].append(False)
            st.session_state.gameover_feedback = f'''"{st.session_state.guess}" is not correct.
                                                     \n\n**GAME OVER**: You ran out of lives! Please start a new game.
                                                     \n\nThe correct answer was **{st.session_state.correct_song}**, {st.session_state.correct_section}, from the album **{st.session_state.correct_album}**.'''
            end_game()
            st.rerun()
    st.session_state.guess = None

def hint():
    st.session_state.hints += 1
    st.session_state.hints_used += 1
    st.session_state.points -= 1

    if st.session_state.hints == 1: 
        st.session_state.hint_feedback += f"Hint 1: this song comes from the album **{st.session_state.correct_album}**"
    if st.session_state.hints == 2: 
        st.session_state.hint_feedback += f'\n\nHint 2: the next line of this song is "*{st.session_state.next_line}*"'
    if st.session_state.hints == 3: 
        st.session_state.disable_hint_btn = True
        st.session_state.hint_feedback += f'\n\nHint 3: the previous line of this song is "*{st.session_state.prev_line}*"'

def giveup():
    st.session_state.disable_buttons = True
    st.session_state.disable_hint_btn = True
    st.session_state.points -= 2
    st.session_state.lives -= 1
    st.session_state.round_results.append(False)
    st.session_state.streaks.append(st.session_state.streak)
    st.session_state.streak = 0
    st.session_state.album_counter[st.session_state.correct_album].append(False)

    st.session_state.giveup_feedback = f"""The correct answer was **{st.session_state.correct_song}**, {st.session_state.correct_section}, from the album **{st.session_state.correct_album}**\n\nYou lost 2 points and have {st.session_state.points} points left."""        

    if st.session_state.game_mode == "Survival (with 3 lives)":
        st.session_state.giveup_feedback += f"\n\nYou lost a life and have {st.session_state.lives} lives left."
        if st.session_state.lives == 0: 
            st.session_state.gameover_feedback = f'**GAME OVER**: You ran out of lives! Please start a new game.'
            end_game()
            return

def end_game():
    accuracy_pct = round((sum(st.session_state.round_results) * 100 /st.session_state.round_count), 2)
    possible_pct = round(st.session_state.points * 100 / (st.session_state.round_count * POINTS_MAPPING[st.session_state.difficulty]), 2)
    accuracy_str = f"{sum(st.session_state.round_results)}/{st.session_state.round_count} ({accuracy_pct}%)"
    possible_str = f"{st.session_state.points}/{st.session_state.round_count * POINTS_MAPPING[st.session_state.difficulty]} ({possible_pct}%)"

    accs = {album: (round(sum(ls) * 100/len(ls), 3), sum(ls), len(ls)) 
            if len(ls) else (0, 0, 0) for album, ls in st.session_state.album_counter.items()}
    st.session_state.album_accs = dict(sorted(accs.items(), 
                                       key=lambda x: (x[1][0], x[1][2], x[1][1]),
                                       reverse=True))
    
    st.session_state.past_game_stats = f"""
{DIFFICULTY_MAPPING[st.session_state.difficulty]} difficulty, {st.session_state.round_count} rounds played
* :dart: Accuracy: {accuracy_str}
* :100: Points out of total possible: {possible_str}
* :bulb: Hints used: {st.session_state.hints_used}
* :fire: Max streak: {max(st.session_state.streaks) if len(st.session_state.streaks) else 0}
* :moneybag: Total points: {st.session_state.points}
"""
    # the feedback is gonna disappear, probably - so might want to display them again until start button clicked
    # and they are all zeroed out again
    st.session_state.game_in_progress = False

### UI ###
if st.session_state.game_in_progress == False: 

    start_tab, leaderboard_tab = st.tabs(["Start New Game", "Leaderboard"])

    with start_tab: 
        with st.form("game_settings"):
            st.markdown("### Start a New Game")
            st.selectbox("Select a game difficulty", 
                         options=DIFFICULTIES,
                         key="difficulty0")
            st.selectbox("Select a game mode",
                         options=GAME_MODES,
                         key="game_mode0")
            with st.expander("Advanced options"):
                st.multiselect("Select albums to generate lyrics from",
                               options=ALL_ALBUMS,
                               default=ALL_ALBUMS,
                               key="albums0")
            st.form_submit_button(":large_green_square: Start new game",
                                  on_click=game_started,
                                  kwargs=dict(difficulty=st.session_state.difficulty0,
                                              game_mode=st.session_state.game_mode0,
                                              albums=st.session_state.albums0))
            
        if st.session_state.gameover_feedback: 
            st.error(st.session_state.gameover_feedback, icon="😢")
            
        if st.session_state.hint_feedback:
            st.info(f"{st.session_state.hint_feedback}", icon="ℹ️")

        if st.session_state.incorrect_feedback:
            st.error(f"{st.session_state.incorrect_feedback}", icon="🚨")

        if st.session_state.correct_feedback:
            st.success(f"{st.session_state.correct_feedback}", icon="✅")
        
        if st.session_state.giveup_feedback:
            st.error(f"{st.session_state.giveup_feedback}", icon="🚨")

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
        
        col1, col2, col3, col4 = st.columns([1.5, 3, 1, 1])
        hint_btn = col1.button(":bulb: Hint", on_click=hint, disabled=st.session_state.disable_hint_btn, help="")
        giveup_btn = col2.button(":no_entry: Give up", on_click=giveup, 
                                 disabled=st.session_state.disable_buttons,
                                 help="2 points are deducted from your total if you give up.")
        
        if st.session_state.hint_feedback:
            st.info(f"{st.session_state.hint_feedback}", icon="ℹ️")

        if st.session_state.incorrect_feedback:
            st.error(f"{st.session_state.incorrect_feedback}", icon="🚨")

        if st.session_state.correct_feedback:
            st.success(f"{st.session_state.correct_feedback}", icon="✅")
            st.button(":arrow_right: Next round", on_click=new_round)
        
        if st.session_state.giveup_feedback:
            st.error(f"{st.session_state.giveup_feedback}", icon="🚨")
            st.button(":arrow_right: Next round", on_click=new_round)
        
        col1, col2, col4 = st.columns(3)
        col4.button(":octagonal_sign: End current game", on_click=end_game, key="end_game")

print(f"difficulty {st.session_state.difficulty}")