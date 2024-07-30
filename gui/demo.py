import streamlit as st

# Initialize session state for form submission and page navigation
if 'form_submitted' not in st.session_state:
    st.session_state['form_submitted'] = False

def submit_form():
    st.session_state['form_submitted'] = True

# Conditional rendering based on form submission
if not st.session_state['form_submitted']:
    # Display the form
    with st.container(border=True):
        with st.form(key='my_form'):
            select_box = st.selectbox('Choose an option', ['Option 1', 'Option 2', 'Option 3'], key='box')
            submit_button = st.form_submit_button(label='Submit', on_click=submit_form)
else:
    # Display the main part of the app (e.g., the game)
    with st.container(border=True):
        st.write("# Main Part of the App")
        st.write("You selected:", st.session_state.box)
        st.write("Now you can play the game!")

# You can still access the value of the select box from the session state
if 'box' in st.session_state:
    st.write("Select box value is still available:", st.session_state.box)
