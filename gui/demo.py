import streamlit as st
from streamlit_option_menu import option_menu

# Define themes with their respective CSS styles
themes = {
    "Light": {
        "background_color": "#ffffff",
        "text_color": "#000000",
        "font_family": "Arial, sans-serif"
    },
    "Dark": {
        "background_color": "#333333",
        "text_color": "#ffffff",
        "font_family": "Courier New, monospace"
    },
    "Blue": {
        "background_color": "#e0f7fa",
        "text_color": "#00796b",
        "font_family": "Verdana, sans-serif"
    }
}

# Function to inject custom CSS based on the selected theme
def apply_theme(theme):
    css = f"""
    <style>
    .stApp {{
        background: {theme['background_color']}
    }}
    .stButton>button {{
        background-color: {theme['text_color']};
        color: {theme['background_color']};
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Create a sidebar menu for theme selection
with st.sidebar:
    selected_theme = option_menu(
        "Select Theme",
        options=list(themes.keys()),
        icons=["sun", "moon", "palette"],
        menu_icon="brush",
        default_index=0
    )

# Apply the selected theme
apply_theme(themes[selected_theme])

# Your Streamlit app content
st.title("Themed Streamlit App")
st.write("This is an example of a Streamlit app with theme selection.")
st.button("Click Me")

# Display the current theme
st.sidebar.write(f"Current theme: {selected_theme}")