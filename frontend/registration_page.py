import streamlit

import backend.postgres_api as postgres


def render_registration_page():
    streamlit.title("Create your Chirper account")

    with streamlit.form("registration_form"):
        username = streamlit.text_input("Username")
        password = streamlit.text_input("Password", type="password")
        confirm_password = streamlit.text_input("Confirm password", type="password")
        submitted = streamlit.form_submit_button("Create account")

    if submitted:
        username = username.strip()
        if not username or not password:
            streamlit.error("Username and password are required.")
        elif password != confirm_password:
            streamlit.error("Passwords do not match.")
        elif postgres.fetch_user_by_username(username) is not None:
            streamlit.error("That username is already taken.")
        else:
            user_id = postgres.create_user(username, password)
            streamlit.session_state.logged_in = True
            streamlit.session_state.user_id = user_id
            streamlit.session_state.username = username
            streamlit.session_state.page = "home"
            streamlit.rerun()

    if streamlit.button("⬅️ Back to log in"):
        streamlit.session_state.page = "login"
        streamlit.rerun()
