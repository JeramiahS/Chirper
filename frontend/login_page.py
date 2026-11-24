import streamlit

# Initialize session state for login status
if "logged_in" not in streamlit.session_state:
    streamlit.session_state.logged_in = False


def login_page():
    streamlit.title("Chirper")

    # Use a form so the page doesn't rerun on every keystroke
    with streamlit.form("login_form"):
        username = streamlit.text_input("Username")
        password = streamlit.text_input("Password", type="password")
        submit = streamlit.form_submit_button("Log In")

        if submit:
            # Replace with streamlit.secrets or a secure database lookup in production
            if username == "admin" and password == "password123":
                streamlit.session_state.logged_in = True
                streamlit.rerun()
            else:
                streamlit.error("Invalid username or password")


def logout():
    streamlit.session_state.logged_in = False
    streamlit.rerun()


# Gatekeeper: Stop execution if not logged in
if not streamlit.session_state.logged_in:
    login_page()
    streamlit.stop()

# --- Protected App Content Below ---
streamlit.sidebar.button("Log Out", on_click=logout)
streamlit.title("Welcome to the Dashboard")
streamlit.write("You are viewing protected content.")
