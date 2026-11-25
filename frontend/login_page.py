import streamlit

import backend.postgres_api as postgres


def render_login_page():
    streamlit.title("Chirper")

    with streamlit.form("login_form"):
        username = streamlit.text_input("Username")
        password = streamlit.text_input("Password", type="password")
        submitted = streamlit.form_submit_button("Log In")

    if submitted:
        user = postgres.fetch_user_by_username(username.strip())
        if user is not None and user[2] == password:
            streamlit.session_state.logged_in = True
            streamlit.session_state.user_id = user[0]
            streamlit.session_state.username = user[1]
            streamlit.session_state.page = "home"
            streamlit.rerun()
        else:
            streamlit.error("Invalid username or password")

    if streamlit.button("📝 Register"):
        streamlit.session_state.page = "register"
        streamlit.rerun()
