import streamlit as st 
import pandas as pd
import numpy as np

from server_tools.Lyrics import Lyrics

# TODO: possibly add leaderboard? Only if all albums selected tho. some sort of database

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
# TODO: preliminary theme names - add emojis and fonts later!
themes = ["Debut", 
          "Fearless", 
          "Speak Now", 
          "Red",
          "1989", 
          "reputation",
          "Lover",
          "folklore",
          "evermore",
          "Midnights",
          "TTPD"]
theme_css = {
    "Debut": {
        "background_color": "#006767",
        "button_color": "#597A5D", 
        "inputs": "#4A786D", 
        "text_color": "white"
    },
    "Fearless": {
        "background_color": "BurlyWood", 
        "button_color": "#D0B38E",
        "inputs": "Wheat",
        "text_color": "black"
    }, 
    "Speak Now": {
        "background_color": "#8B698E",
        "button_color": "#86469C",
        "inputs": "#BB9AB1",
        "text_color": "white"
    },
    "Red": {
        "background_color": "#7D2727",
        "button_color": "#755B48",
        "inputs": "#5F2020",
        "text_color": "white"
    },
    "1989": {
        "background_color": "#8A96AE",
        "button_color": "#ccc4c2",
        "inputs": "#748CA9",
        "text_color": "black"
    },
    "reputation": {
        "background_color": "#222222",
        "button_color": "#000000",
        "inputs": "#4C4949",
        "text_color": "white"
    }, 
    "Lover": {
        "background_color": "#D39DA9",
        "button_color": "#CC7CA3",
        "inputs": "#FCBDC4",
        "text_color": "black"
    }, 
    "folklore": {
        "background_color": "#7f7f7f",
        "button_color": "#616161",
        "inputs": "#353535",
        "text_color": "white"
    },
    "evermore": {
        "background_color": "#643325",
        "button_color": "#7f3c10	",
        "inputs": "#895A38",
        "text_color": "white"
    },
    "Midnights": {
        "background_color": "#212145",
        "button_color": "#1D1D34",
        "inputs": "#4e4466",
        "text_color": "white"
    },
    "TTPD": {
        "background_color": "#a79e8f",
        "button_color": "#6f6a66",
        "inputs": "#9A9181",
        "text_color": "black"
    }
            }

# TODO: initiate session state stuff via loop w/ list (exc. lyrics)
if "lyrics" not in st.session_state: 
    st.session_state.lyrics = Lyrics(data=all_lyrics)
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
if "game_over_msg" not in st.session_state: 
    st.session_state.game_over_msg = ""
if "hint_str" not in st.session_state: 
    st.session_state.hint_str = ""
if "giveup_str" not in st.session_state: 
    st.session_state.giveup_str = ""
if "correct_str" not in st.session_state: 
    st.session_state.correct_str = ""
if "incorrect_str" not in st.session_state: 
    st.session_state.incorrect_str = ""
if "album_counter" not in st.session_state: 
    st.session_state.album_counter = None
if "album_accs" not in st.session_state:
    st.session_state.album_accs = None

def apply_theme(selected_theme):
    css = f"""
    <style>
    .stApp > header {{
        background-color: transparent;
    }}
    .eczjsme16 {{ 
        background: {selected_theme['background_color']};
    }}
    .stApp {{
        background: {selected_theme['background_color']};
        color: {selected_theme["text_color"]};
        font-family: "Helvetica", "Arial", sans-serif;
    }}
    button {{
        background-color: {selected_theme['button_color']} !important;
    }}
    button:disabled {{
        background-color: transparent !important;
    }}
    .st-d8, .st-fg {{
        background-color: {selected_theme['inputs']} !important;
        color: {selected_theme["text_color"]};
        border-radius: 10px;
    }}
    p, ul {{
        color: {selected_theme["text_color"]};
        font-weight: 600 !important;
    }}
    h3, h2, h1, strong, .lyrics {{
        color: {selected_theme["text_color"]};
        font-weight: 900 !important;
    }}
    .lyrics {{
        font-size: 18px;
    }}
    .st-cb {{
        color: {selected_theme["text_color"]};
    }}
    .st-gg {{
        -webkit-text-fill-color: {selected_theme["text_color"]}
    }}
    [data-baseweb="tag"] {{
        background: {selected_theme['button_color']} !important;
        color: {selected_theme["text_color"]};
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# TODO: casual docstrings 
def reset_album_counter():
    st.session_state.album_counter = {album_name: [] for album_name in st.session_state.albums}

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
    st.session_state.game_over_msg = ""
    st.session_state.hint_str = ""
    st.session_state.giveup_str = ""
    st.session_state.correct_str = ""
    st.session_state.incorrect_str = ""

    generated_lyrics = f'<div class="lyrics">{st.session_state.lyrics.generate(mode)}</div>'
    correct_song = st.session_state.lyrics.get_track_name()
    correct_album = st.session_state.lyrics.get_album_name()
    next_line = st.session_state.lyrics.get_next_line()
    prev_line = st.session_state.lyrics.get_previous_line()
    section = st.session_state.lyrics.get_section()

    return generated_lyrics, correct_song, correct_album, next_line, prev_line, section

def end_current_game(): 
    if st.session_state.round_count:
        accuracy_pct = round((st.session_state.correct_rounds_count / st.session_state.round_count), 2) * 100
        possible_pct = (st.session_state.points / (st.session_state.round_count * points_mapping[mode])) * 100

        accs = {album: (round(sum(ls)/len(ls), 3) * 100, sum(ls), len(ls)) if len(ls) else (0, 0, 0) for album, ls in st.session_state.album_counter.items()}
        st.session_state.album_accs = dict(sorted(accs.items(), 
                                                  key=lambda x: (x[1][0], x[1][2], x[1][1]),
                                                  reverse=True))

        st.session_state.past_game_scores = f"""
    {mode_mapping[mode]} difficulty, {st.session_state.round_count} rounds played
    * :dart: Accuracy: {st.session_state.correct_rounds_count}/{st.session_state.round_count} ({accuracy_pct}%)
    * :100: Points out of total possible: {st.session_state.points}/{st.session_state.round_count * points_mapping[mode]} ({round(possible_pct, 2)}%)
    * :fire: Max streak: {max(st.session_state.streaks) if len(st.session_state.streaks) else 0}
    * :moneybag: :green[Total points: {st.session_state.points}]
    """
    st.session_state.streak = 0
    st.session_state.streaks = []
    st.session_state.disable_start_btn = False
    st.session_state.show_lyrics = False
    st.session_state.points = 0
    st.session_state.round_count = 0
    st.session_state.correct_rounds_count = 0
    st.session_state.guess = ""
    st.session_state.hint_str = ""
    st.session_state.giveup_str = ""
    st.session_state.correct_str = ""
    st.session_state.incorrect_str = ""

def disable_start_button(): 

    if len(st.session_state.albums) == 0: 
        start_form.error("Please select at least one album.")
    else: 
        st.session_state.disable_start_btn = True
        st.session_state.lives = 3

        filtered_lyrics = all_lyrics[all_lyrics["album_name"].isin(st.session_state.albums)].reset_index()
        st.session_state.lyrics = Lyrics(data=filtered_lyrics)
    
    reset_album_counter()
    

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
    st.session_state.album_counter[st.session_state.correct_album].append(False)
    st.session_state.giveup_str = f"The correct answer was **{st.session_state.correct_song}**, {st.session_state.correct_section}, from the album **{st.session_state.correct_album}**"        
    if game_mode == "Survival (with 3 lives)":
        st.session_state.giveup_str = st.session_state.giveup_str + f"\n\nYou lost a life and have {st.session_state.lives} lives left."
        if st.session_state.lives == 0: 
            st.session_state.game_over_msg = f'**GAME OVER**: You ran out of lives! Please start a new game.\n\nThe correct answer was **{st.session_state.correct_song}**, {st.session_state.correct_section}, from the album **{st.session_state.correct_album}**.'
            end_current_game()
            return

def add_hint(): 
    st.session_state.hint_count += 1
    st.session_state.points -= 1
    if st.session_state.hint_count == 1: 
        st.session_state.hint_str += f"Hint 1: this song comes from the album **{st.session_state.correct_album}**"
    if st.session_state.hint_count == 2: 
        st.session_state.hint_str += f'\n\nHint 2: the next line of this song is "*{st.session_state.next_line}*"'
    if st.session_state.hint_count == 3: 
        st.session_state.disable_hint_btn = True
        st.session_state.hint_str += f'\n\nHint 3: the previous line of this song is "*{st.session_state.prev_line}*"'

def answered_correctly(): 
    st.session_state.correct_str = f"That is correct! The answer is indeed **{st.session_state.correct_song}**, {st.session_state.correct_section}, from the album **{st.session_state.correct_album}**. Well done!"
    st.session_state.points += points_mapping[mode]
    st.session_state.correct_rounds_count += 1
    st.session_state.guess = None
    st.session_state.disable_hint_btn = True
    st.session_state.disable_giveup_btn = True
    st.session_state.disable_guess_input = True
    st.session_state.streak += 1
    st.session_state.incorrect_str = ""
    st.session_state.album_counter[st.session_state.correct_album].append(True)

def answered_incorrectly(game_mode): 
    st.session_state.incorrect_str = f'"{st.session_state.guess}" is not correct. Please try again!'
    st.session_state.points -= 1
    st.session_state.lives -= 1
    st.session_state.guess = None
    st.session_state.streaks.append(st.session_state.streak)
    st.session_state.streak = 0
    if game_mode == "Survival (with 3 lives)":
        st.session_state.incorrect_str = st.session_state.incorrect_str + f"\n\nYou lost a life and have {st.session_state.lives} lives left."
        if st.session_state.lives == 0: 
            st.session_state.disable_guess_input = True
            st.session_state.disable_giveup_btn = True
            st.session_state.disable_hint_btn = True
            st.session_state.album_counter[st.session_state.correct_album].append(False)
            st.session_state.game_over_msg = f'"{st.session_state.guess}" is not correct.\n\n**GAME OVER**: You ran out of lives! Please start a new game.\n\nThe correct answer was **{st.session_state.correct_song}**, {st.session_state.correct_section}, from the album **{st.session_state.correct_album}**.'
            end_current_game()
            st.rerun()
            return    

st.title("Welcome to :sparkles:tayLyrics:sparkles:!")

# SIDEBAR #
with st.sidebar: 
    with st.expander(":pencil2: Instructions"): 
        st.markdown(f"Lyrics range from debut to *{all_albums[-1]}*.")
        st.info('IMPORTANT: \n\nDo NOT include "(Taylor\'s Version)" in your guesses; e.g. "Back to December (Taylor\'s Version)" should simply be "Back to December."\n\nAnswer "All Too Well" for BOTH the 5-minute and 10-minute versions of All Too Well.', icon="ℹ️")

        selected_theme = st.radio("Select a theme",
                                  options=themes)
        apply_theme(theme_css[selected_theme])

    start_form = st.form("game_settings")
    with start_form:
        mode = st.selectbox("Select a game difficulty", 
                            options=mode_options, 
                            disabled=st.session_state.disable_start_btn)
        game_mode = st.selectbox("Select a game mode", 
                                 options=gamemode_options,
                                 disabled=st.session_state.disable_start_btn)
        with st.expander("Advanced options"):
            st.multiselect("Select albums to generate lyrics from", 
                            options=all_albums, 
                            default=all_albums, 
                            disabled=st.session_state.disable_start_btn, 
                            key="albums")
        start_btn = st.form_submit_button(":large_green_square: Start new game", disabled=(st.session_state.disable_start_btn),
                                          on_click=disable_start_button)

# MAIN PANEL #
if (start_btn and len(st.session_state.albums)) or st.session_state.next: 
    st.session_state.generated_lyrics, st.session_state.correct_song, st.session_state.correct_album, st.session_state.next_line, st.session_state.prev_line, st.session_state.correct_section = new_round(mode=mode)

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
        col3.button(":octagonal_sign: End current game", on_click=end_current_game, key="end_game")
        # TODO: may be a way to clean this up
        if st.session_state.hint_str:
            st.info(f"{st.session_state.hint_str}", icon="ℹ️")
        if st.session_state.correct_str:
            st.success(f"{st.session_state.correct_str}", icon="✅")
            container.button(":arrow_right: Next round", on_click=next_round)
        if st.session_state.incorrect_str:
            st.error(f"{st.session_state.incorrect_str}", icon="🚨")
        if st.session_state.giveup_str:
            st.error(f"{st.session_state.giveup_str}", icon="🚨")
            container.button(":arrow_right: Next round", on_click=next_round)
    else: 
        st.markdown('Click the "Start new game" button to start guessing!')
        if st.session_state.past_game_scores: 
            st.markdown("### Past Game Statistics")
            st.markdown(st.session_state.past_game_scores)
        if st.session_state.game_over_msg:
            st.error(st.session_state.game_over_msg, icon="😢")
        with st.expander("**Per-album accuracies**"):
            s = ""
            for album_name, tup in st.session_state.album_accs.items(): 
                s += f"* {album_name}: {tup[0]}% ({tup[1]}/{tup[2]})\n"
            st.markdown(s)
        # TODO: option for leaderboard
        # if st.session_state.albums: 
        #     with st.popover("Add to leaderboard"):
        #         st.markdown(f"Save your results to the tayLyrics leaderboard!")
        #         # TODO: text area. actual logistics of leaderboard

st.sidebar.divider()
with st.sidebar.container(border=True):
    st.markdown("### Game Statistics")
    st.markdown(f"**{mode_mapping[mode]} difficulty, {game_mode} mode**")

    if st.session_state.round_count: 
        st.markdown(f"* :large_green_circle: Round: {st.session_state.round_count}")
        accuracy_pct = round((st.session_state.correct_rounds_count / st.session_state.round_count), 2) * 100
        st.markdown(f"* :dart: Accuracy: {st.session_state.correct_rounds_count}/{st.session_state.round_count} ({accuracy_pct}%)")
        possible_pct = (st.session_state.points / (st.session_state.round_count * points_mapping[mode])) * 100
        st.markdown(f"* :100: Points out of total possible: {st.session_state.points}/{st.session_state.round_count * points_mapping[mode]} ({round(possible_pct, 2)}%)")
        st.markdown(f"* :fire: Current streak: {st.session_state.streak}")
        st.markdown(f"* :moneybag: :green[Total points: {st.session_state.points}]")
    if game_mode == "Survival (with 3 lives)":
        st.markdown(f"* :space_invader: :red[Lives: {st.session_state.lives}]")